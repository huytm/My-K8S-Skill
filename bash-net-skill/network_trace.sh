#!/bin/bash

# Nhận tham số đầu tiên là tên Pod
TARGET_POD=$1

if [ -z "$TARGET_POD" ]; then
    echo '{"status": "error", "message": "Missing target pod name"}'
    exit 1
fi

# Tại đây bạn có thể gọi các lệnh thực tế trong container của agent
# Ví dụ: chạy ovnkube-trace để kiểm tra luồng mạng của Pod trong cluster
# ovnkube-trace -namespace default -pod $TARGET_POD ...
echo "Executed at $(date)" >> /tmp/skill_test.log
# Trong bài lab này, ta giả lập kết quả trả về
TRACE_RESULT="Trace execution simulated for $TARGET_POD"

# Output BẮT BUỘC phải in ra stdout (thường là định dạng JSON để agent dễ đọc)
echo "{\"status\": \"success\", \"pod\": \"$TARGET_POD\", \"action\": \"ovnkube-trace\", \"details\": \"$TRACE_RESULT\"}"
