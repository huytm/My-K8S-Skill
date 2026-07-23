#!/usr/bin/env python3
import sys
import json

def main():
    # Kiểm tra xem kagent có truyền argument vào không
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing JSON payload argument"}))
        sys.exit(1)
        
    raw_payload = sys.argv[1]
    
    # Parse dữ liệu JSON
    try:
        data = json.loads(raw_payload)
        alerts = data.get("alerts", [])
        alert_count = len(alerts)
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON format"}))
        sys.exit(1)

    # Trả kết quả về cho agent xử lý tiếp
    result = {
        "status": "success",
        "processed_alerts": alert_count,
        "action": "webhook_parsed",
        "original_payload_keys": list(data.keys())
    }
    
    # In ra stdout
    print(json.dumps(result))

if __name__ == "__main__":
    main()
