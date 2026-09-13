"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent)
"""

import json
from typing import Dict, Any, List

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu phòng họp trống
    {
        "name": "check_room_availability",
        "description": "Kiểm tra danh sách phòng họp còn trống theo ngày, khung giờ và sức chứa tối thiểu.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Ngày cần kiểm tra phòng theo định dạng YYYY-MM-DD hoặc DD/MM/YYYY (ví dụ: '2026-09-15')"
                },
                "time_slot": {
                    "type": "string",
                    "description": "Khung giờ cần họp (ví dụ: '09:00-11:00', '14:00-16:00')"
                },
                "min_capacity": {
                    "type": "integer",
                    "description": "Số lượng người tham gia tối thiểu cần chứa (ví dụ: 10)"
                }
            },
            "required": ["date", "time_slot"]
        }
    },
    
    # Tool 2: Đặt phòng họp và thiết bị
    {
        "name": "book_meeting_room",
        "description": "Đặt phòng họp và yêu cầu các thiết bị đi kèm (máy chiếu, micro, whiteboard) cho người dùng.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã định danh phòng họp (ví dụ: 'P301', 'P502')"
                },
                "booker_name": {
                    "type": "string",
                    "description": "Họ và tên hoặc mã người đặt phòng (ví dụ: 'Nguyễn Văn An')"
                },
                "date": {
                    "type": "string",
                    "description": "Ngày đặt phòng (ví dụ: '2026-09-15')"
                },
                "time_slot": {
                    "type": "string",
                    "description": "Khung giờ họp (ví dụ: '14:00-16:00')"
                },
                "equipments": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Danh sách thiết bị cần mượn (ví dụ: ['projector', 'micro', 'whiteboard'])"
                }
            },
            "required": ["room_id", "booker_name", "date", "time_slot"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_ROOMS = [
    {
        "room_id": "P301",
        "room_name": "Phòng Hội Thảo A",
        "capacity": 20,
        "available_equipments": ["projector", "micro", "whiteboard", "tv"],
        "booked_slots": {
            "2026-09-15": ["08:00-10:00", "13:00-15:00"]
        }
    },
    {
        "room_id": "P302",
        "room_name": "Phòng Họp Nhỏ",
        "capacity": 8,
        "available_equipments": ["whiteboard", "tv"],
        "booked_slots": {
            "2026-09-15": []
        }
    },
    {
        "room_id": "P501",
        "room_name": "Phòng Hội Nghị Lớn",
        "capacity": 50,
        "available_equipments": ["projector", "micro", "whiteboard", "video_conference"],
        "booked_slots": {
            "2026-09-15": ["09:00-11:00"]
        }
    }
]


def execute_check_room_availability(date: str, time_slot: str, min_capacity: int = 1) -> str:
    """Thực thi kiểm tra phòng họp trống theo tiêu chí"""
    available_rooms = []
    
    for room in MOCK_ROOMS:
        if room["capacity"] < min_capacity:
            continue
        
        booked_times = room["booked_slots"].get(date, [])
        if time_slot not in booked_times:
            available_rooms.append({
                "room_id": room["room_id"],
                "room_name": room["room_name"],
                "capacity": room["capacity"],
                "available_equipments": room["available_equipments"]
            })
            
    if available_rooms:
        return json.dumps({
            "status": "SUCCESS",
            "date": date,
            "time_slot": time_slot,
            "total_available": len(available_rooms),
            "rooms": available_rooms
        }, ensure_ascii=False)
        
    return json.dumps({
        "status": "NOT_FOUND",
        "date": date,
        "time_slot": time_slot,
        "message": f"Không có phòng nào phù hợp với sức chứa từ {min_capacity} người trong khung giờ {time_slot} ngày {date}."
    }, ensure_ascii=False)


def execute_book_meeting_room(room_id: str, booker_name: str, date: str, time_slot: str, equipments: List[str] = None) -> str:
    """Thực thi đặt phòng họp và trang thiết bị"""
    equipments = equipments or []
    room = next((r for r in MOCK_ROOMS if r["room_id"].upper() == room_id.strip().upper()), None)
    
    if not room:
        return json.dumps({
            "status": "ERROR",
            "message": f"Mã phòng '{room_id}' không tồn tại trong hệ thống."
        }, ensure_ascii=False)
        
    # Kiểm tra xung đột lịch
    booked_times = room["booked_slots"].get(date, [])
    if time_slot in booked_times:
        return json.dumps({
            "status": "CONFLICT",
            "message": f"Phòng {room_id} đã có người đặt trong khung giờ {time_slot} ngày {date}."
        }, ensure_ascii=False)
        
    # Tạo mã đặt phòng
    booking_ref = f"FAC-{room_id}-{date.replace('-', '')}-BK"
    
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": booking_ref,
        "room_id": room["room_id"],
        "room_name": room["room_name"],
        "booker": booker_name,
        "date": date,
        "time_slot": time_slot,
        "reserved_equipments": equipments,
        "message": f"Đặt phòng {room['room_name']} ({room_id}) thành công cho {booker_name} vào lúc {time_slot} ngày {date}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "check_room_availability": execute_check_room_availability,
    "book_meeting_room": execute_book_meeting_room
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)