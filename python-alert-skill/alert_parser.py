#!/usr/bin/env python3
import sys
import json
import logging
from datetime import datetime

# ---------------------------------------------------------
# Cấu hình Logging
# ---------------------------------------------------------
logger = logging.getLogger("AlertParserSkill")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

# 1. Luôn thêm StreamHandler ghi ra stderr (An toàn nhất trên Container/K8s)
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)

# 2. Thử ghi vào file local, nếu không có quyền ghi thì bỏ qua (tránh crash script)
LOG_FILE = "/tmp/alert_parser.log"
try:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"Không thể tạo file log local tại {LOG_FILE}: {e}")

# ---------------------------------------------------------
# Logic chính của Script
# ---------------------------------------------------------
def main():
    logger.info("=== Bắt đầu thực thi alert_parser.py ===")
    
    # Kiểm tra tham số truyền vào từ kagent
    if len(sys.argv) < 2:
        error_msg = "Thiếu tham số truyền vào (JSON payload)"
        logger.error(error_msg)
        
        # In kết quả JSON lỗi ra stdout cho Agent đọc
        print(json.dumps({"status": "error", "message": error_msg}))
        sys.exit(1)
        
    raw_payload = sys.argv[1]
    logger.debug(f"Input payload nhận được từ Agent: {raw_payload}")
    
    # Parse dữ liệu JSON
    try:
        data = json.loads(raw_payload)
        alerts = data.get("alerts", [])
        alert_count = len(alerts)
        logger.info(f"Parse JSON thành công. Số lượng alert tìm thấy: {alert_count}")
        
    except json.JSONDecodeError as e:
        error_msg = f"Lỗi cú pháp JSON: {str(e)}"
        logger.error(error_msg)
        
        print(json.dumps({"status": "error", "message": error_msg}))
        sys.exit(1)

    # Chuẩn bị kết quả trả về
    result = {
        "status": "success",
        "processed_alerts": alert_count,
        "action": "webhook_parsed",
        "original_payload_keys": list(data.keys()),
        "exec_timestamp": datetime.now().isoformat()
    }
    
    logger.info("Xử lý hoàn tất, đang trả kết quả JSON về stdout...")
    logger.info("=== Kết thúc thực thi ===")

    # In kết quả JSON DUY NHẤT ra stdout
    print(json.dumps(result))

if __name__ == "__main__":
    main()
