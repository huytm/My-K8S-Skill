# QUY ĐỊNH XỬ LÝ SỰ CỐ K8S NỘI BỘ
1. Khi phát hiện một Pod bị lỗi, bước ĐẦU TIÊN tuyệt đối không được xóa Pod, mà phải gắn nhãn (label) cho nó là `status=quarantine` để cô lập.
2. Bước thứ HAI là phải chụp lại trạng thái bằng lệnh `kubectl describe`.
3. Bước thứ BA là nhắn một câu thông báo vào nhóm Slack với cú pháp: "[ALERT] Phát hiện lỗi tại Pod X, đã cô lập để kiểm tra".
