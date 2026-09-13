"""
🖥️ GIAO DIỆN STREAMLIT CHO FACILITIES REACT AGENT
Hiển thị giao diện Chat và Luồng suy luận (Thought -> Action -> Observation)
"""

import sys
import os
import json
import streamlit as st

# Thêm thư mục hiện tại vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers import get_llm_provider
from mcp_server import MCPAcademicServer
from prompts import REACT_AGENT_SYSTEM_PROMPT, MAX_ITERATIONS

st.set_page_config(
    page_title="Facilities ReAct Agent",
    page_icon="🏢",
    layout="wide"
)

# Khởi tạo Provider và Server một lần duy nhất
@st.cache_resource
def init_agent():
    provider = get_llm_provider()
    mcp_server = MCPAcademicServer()
    return provider, mcp_server

provider, mcp_server = init_agent()

# Tiêu đề ứng dụng
st.title("🏢 Facilities Assistant (ReAct + MCP)")
st.caption(f"Provider: **{provider.__class__.__name__}** | MCP Server: **{mcp_server.server_name}**")

# Khởi tạo session state lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Tôi có thể giúp bạn tra cứu phòng họp trống hoặc đặt phòng và thiết bị. Bạn cần hỗ trợ gì?", "traces": []}
    ]

# Chia 2 cột: Cột trái Chat, Cột phải Trace Log
col_chat, col_trace = st.columns([6, 4])

with col_chat:
    st.subheader("💬 Hội thoại")
    
    # Hiển thị các tin nhắn cũ
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Xử lý input từ người dùng
    user_input = st.chat_input("Nhập yêu cầu (ví dụ: Tìm phòng cho 15 người ngày 2026-09-15 14:00-16:00)...")

    if user_input:
        # Thêm tin nhắn user vào màn hình
        st.session_state.messages.append({"role": "user", "content": user_input, "traces": []})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Chạy vòng lặp ReAct
        step = 0
        current_traces = []
        tools_list = mcp_server.list_tools()
        final_answer = ""

        with st.chat_message("assistant"):
            with st.spinner("Agent đang suy luận..."):
                while step < MAX_ITERATIONS:
                    step += 1
                    llm_response = provider.generate_with_tools(user_input, tools_list, system_prompt=REACT_AGENT_SYSTEM_PROMPT)
                    thought = llm_response.get("thought", "Đang suy luận...")

                    if llm_response.get("type") == "text":
                        final_answer = llm_response.get("content", "")
                        current_traces.append({
                            "step": step,
                            "thought": thought,
                            "action": "FINAL_ANSWER",
                            "output": final_answer
                        })
                        break

                    elif llm_response.get("type") == "tool_call":
                        tool_name = llm_response.get("tool_name")
                        arguments = llm_response.get("arguments", {})
                        mcp_result = mcp_server.call_tool(tool_name, arguments)
                        obs_data = mcp_result.get("result", {})

                        # Tổng hợp phản hồi
                        if obs_data.get("status") == "SUCCESS":
                            if "rooms" in obs_data:
                                r_list = [f"{r['room_name']} ({r['room_id']} - Chứa: {r['capacity']} người)" for r in obs_data.get("rooms", [])]
                                final_answer = f"Khung giờ **{obs_data.get('time_slot')}** ngày **{obs_data.get('date')}** có {obs_data.get('total_available')} phòng trống:\n- " + "\n- ".join(r_list)
                            elif "booking_id" in obs_data:
                                final_answer = f"✅ {obs_data.get('message')} Mã đặt phòng: `{obs_data.get('booking_id')}`."
                            else:
                                final_answer = json.dumps(obs_data, ensure_ascii=False)
                        else:
                            final_answer = obs_data.get("message", "Thao tác không thành công.")

                        current_traces.append({
                            "step": step,
                            "thought": thought,
                            "action": f"{tool_name}({json.dumps(arguments, ensure_ascii=False)})",
                            "observation": obs_data
                        })
                        break

            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer, "traces": current_traces})
            st.rerun()

# Cột hiển thị Trace Waterfall chi tiết
with col_trace:
    st.subheader("🔍 Trace Waterfall (Suy luận Agent)")
    latest_msg = st.session_state.messages[-1]
    
    if latest_msg["role"] == "assistant" and latest_msg.get("traces"):
        for tr in latest_msg["traces"]:
            with st.expander(f"📍 Step {tr.get('step')}: {tr.get('action')}", expanded=True):
                st.markdown(f"**🧠 Thought:** {tr.get('thought')}")
                if "observation" in tr:
                    st.markdown("**👁️ Observation (MCP Result):**")
                    st.json(tr["observation"])
                if "output" in tr:
                    st.markdown(f"**🏁 Output:** {tr.get('output')}")
    else:
        st.info("Chưa có sự kiện suy luận nào cho câu hỏi này.")