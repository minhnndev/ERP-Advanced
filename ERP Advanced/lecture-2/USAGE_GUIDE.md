# 📘 Hướng dẫn sử dụng nhanh

## 🚀 Cách sử dụng

### Bước 1: Chuẩn bị file Excel

File Excel phải có sheet tên **"Event Logs"** với 4 cột:

| case_id | activity | timestamp | resource |
|---------|----------|-----------|----------|
| ORD001 | Receive Order | 2024-01-15 09:00 | Sales_Nguyen |
| ORD001 | Check Inventory | 2024-01-15 09:15 | Warehouse_Tran |
| ... | ... | ... | ... |

**Yêu cầu:**
- ✅ Sheet tên: `Event Logs`
- ✅ Cột `case_id`: ID của case/đơn hàng/ticket
- ✅ Cột `activity`: Tên hoạt động
- ✅ Cột `timestamp`: Thời gian (định dạng: YYYY-MM-DD HH:MM)
- ✅ Cột `resource`: Người thực hiện

### Bước 2: Chạy phân tích

**Cách 1: Sử dụng file mặc định (event_logs.xlsx)**
```bash
python handover_network_analysis.py
```

**Cách 2: Chỉ định file Excel của bạn**
```bash
python handover_network_analysis.py /path/to/your/file.xlsx
```

**Cách 3: Sử dụng trong Python script**
```python
from handover_network_analysis import main

# Phân tích với file của bạn
main('/path/to/your/event_logs.xlsx')

# Hoặc sử dụng file mặc định
main()
```

### Bước 3: Xem kết quả

Sau khi chạy, bạn sẽ có 3 file kết quả:

1. **handover_network_analysis.png** - Đồ thị visualization
2. **handover_analysis_report.xlsx** - Báo cáo Excel chi tiết
3. **handover_network_interactive.html** - Website tương tác

---

## 📊 Ví dụ dữ liệu

Tôi đã tạo sẵn file **event_logs.xlsx** với quy trình xử lý đơn hàng:

```
6 đơn hàng (cases)
39 events
7 người tham gia
Quy trình: Sales → Warehouse → Manager → Finance → Logistics
```

Bạn có thể:
- ✅ Sử dụng trực tiếp file này để test
- ✅ Sửa đổi file này theo dữ liệu của bạn
- ✅ Tạo file Excel mới theo format tương tự

---

## 🎯 Kết quả phân tích

Chương trình sẽ tính toán:

### 1️⃣ Degree Centrality
- Số lượng kết nối (nhận việc + giao việc)
- Người có nhiều kết nối = Hub trong mạng

### 2️⃣ Betweenness Centrality  
- Chỉ số "Gatekeeper" - kiểm soát luồng công việc
- Người có Betweenness cao = Rất quan trọng cho quy trình

### 3️⃣ Closeness Centrality
- Khả năng tiếp cận nhanh mọi người
- Người có Closeness cao = Coordinator tốt

### 4️⃣ Eigenvector Centrality
- Uy tín dựa trên chất lượng kết nối
- Người có Eigenvector cao = Influencer

### 🏆 Tổng điểm
Kết hợp 4 chỉ số trên để xác định **người quan trọng nhất** trong hệ thống

---

## 💡 Mẹo sử dụng

### Để có kết quả tốt nhất:

1. **Dữ liệu đầy đủ**: Ít nhất 3-5 cases để thấy được pattern
2. **Timestamp chính xác**: Sắp xếp theo thứ tự thời gian
3. **Resource nhất quán**: Đặt tên người thống nhất (VD: Sales_Nguyen, không phải nguyen, Nguyen)

### Customize phân tích:

Bạn có thể điều chỉnh trọng số trong file `handover_network_analysis.py`:

```python
# Dòng 345: Hàm identify_key_person()
total_score = (
    degree_score * 0.25 +        # Thay đổi nếu muốn
    betweenness_score * 0.35 +   # Betweenness quan trọng nhất
    closeness_score * 0.20 +     
    eigenvector_score * 0.20
)
```

---

## 🔧 Troubleshooting

### Lỗi: "Không tìm thấy file"
```
❌ Không tìm thấy file: /path/to/file.xlsx
```
**Giải pháp:** Kiểm tra đường dẫn file có đúng không

### Lỗi: "File Excel thiếu các cột"
```
❌ File Excel thiếu các cột: ['resource']
```
**Giải pháp:** Thêm cột thiếu vào sheet "Event Logs"

### Lỗi: "Sheet 'Event Logs' not found"
```
❌ Sheet 'Event Logs' not found
```
**Giải pháp:** Đổi tên sheet thành "Event Logs" (chính xác)

---

## 📦 Dependencies

```bash
pip install pandas networkx matplotlib seaborn openpyxl
```

---

## 🎨 Interactive Website

Mở file `handover_network_interactive.html` để:
- ✅ Xem đồ thị tương tác (kéo thả các node)
- ✅ Filter theo từng metric (Degree, Betweenness, Closeness, Eigenvector)
- ✅ Hover để xem thông tin chi tiết
- ✅ Bảng xếp hạng top người quan trọng

---

## 📈 Use Cases

Phân tích này hữu ích cho:

1. **Process Mining** - Tìm bottleneck trong quy trình
2. **Resource Planning** - Xác định người cần training backup
3. **Risk Management** - Phát hiện single point of failure
4. **Optimization** - Tối ưu hóa handover giữa các team
5. **Organization Design** - Thiết kế cấu trúc tổ chức hiệu quả

---

## 📞 Support

Nếu cần hỗ trợ:
1. Kiểm tra file Excel có đúng format không
2. Đảm bảo đã cài đủ dependencies
3. Xem log chi tiết khi chạy chương trình

Happy analyzing! 🎉
