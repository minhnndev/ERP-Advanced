# 🔗 Social Network Analysis for Business Process Handover

## 📋 Tổng quan

Dự án này phân tích mạng xã hội trong quy trình giao việc (handover) dựa trên lý thuyết đồ thị và các độ đo Centrality. Mục tiêu là xác định người quan trọng nhất trong hệ thống quy trình nghiệp vụ.

## UI

| Item | Link | Preview |
| --- | --- | --- |
| Graph | [graph-visualize.png](https://github.com/minhnndev/ERP-Advanced/blob/main/ERP%20Advanced/lecture-2/graph-visualize.png) | <img src="https://raw.githubusercontent.com/minhnndev/ERP-Advanced/main/ERP%20Advanced/lecture-2/graph-visualize.png" alt="Graph visualization" width="720" height="420" /> |
| Table | [table-visualize.png](https://github.com/minhnndev/ERP-Advanced/blob/main/ERP%20Advanced/lecture-2/table-visualize.png) | <img src="https://raw.githubusercontent.com/minhnndev/ERP-Advanced/main/ERP%20Advanced/lecture-2/table-visualize.png" alt="Table visualization" width="720" height="420" /> |

## 🎯 Quy trình nghiệp vụ được phân tích

**Tên quy trình:** Xử lý đơn hàng E-commerce

**Các bước chính:**

1. Receive Order (Nhận đơn hàng) - Sales Team
2. Check Inventory (Kiểm tra kho) - Warehouse Team
3. Approve Order (Duyệt đơn) - Manager
4. Process Payment (Xử lý thanh toán) - Finance Team
5. Package Items (Đóng gói) - Warehouse Team
6. Ship Order (Giao hàng) - Logistics Team

**Đặc điểm:**

- 6 cases (đơn hàng) được phân tích
- 39 events logs
- 7 người tham gia
- 15 handover connections

---

## 📊 Các độ đo Centrality

### 1️⃣ Degree Centrality (Độ trung tâm bậc)

**Khái niệm:** Đo lường số lượng kết nối trực tiếp của một nút

**Công thức:**

```
Degree Centrality = (In-Degree + Out-Degree) / (n - 1)
```

**Trong đồ thị Handover:**

- **In-Degree:** Số lần nhận việc từ người khác
- **Out-Degree:** Số lần giao việc cho người khác
- **Total Degree:** Tổng số kết nối

**Ý nghĩa:**

- Người có degree cao = tham gia nhiều handover
- Là "hub" trong mạng lưới
- Có nhiều cơ hội giao tiếp và phối hợp

**Kết quả Top 3:**

1. **Manager_Le:** 0.833 (6 kết nối)
2. **Warehouse_Tran:** 0.833 (5 kết nối)
3. **Warehouse_Dinh:** 0.833 (5 kết nối)

---

### 2️⃣ Betweenness Centrality (Độ trung tâm trung gian)

**Khái niệm:** Đo lường số lần một nút nằm trên đường đi ngắn nhất giữa các nút khác

**Công thức:**

```
Betweenness(v) = Σ (σst(v) / σst)
```

Trong đó:

- σst = số đường đi ngắn nhất từ s đến t
- σst(v) = số đường đi ngắn nhất từ s đến t đi qua v

**Ý nghĩa:**

- Chỉ số "Gatekeeper" - người gác cổng
- Kiểm soát luồng thông tin giữa các nhóm
- Nếu người này nghỉ việc → quy trình có thể bị gián đoạn nghiêm trọng

**Kết quả Top 3:**

1. **Manager_Le:** 0.433 ⭐ GATEKEEPER CHÍNH
2. **Warehouse_Tran:** 0.150
3. **Warehouse_Dinh:** 0.150

**Phân tích:** Manager_Le có Betweenness cao gấp 3 lần người thứ 2, chứng tỏ vai trò cực kỳ quan trọng trong việc kết nối các phòng ban.

---

### 3️⃣ Closeness Centrality (Độ trung tâm gần gũi)

**Khái niệm:** Đo lường mức độ gần gũi với tất cả các nút khác trong mạng

**Công thức:**

```
Closeness(v) = (n - 1) / Σ d(v, u)
```

Trong đó:

- n = số nút
- d(v, u) = khoảng cách ngắn nhất từ v đến u

**Trong đồ thị có hướng:**

- **Closeness In:** Khả năng nhận thông tin nhanh
- **Closeness Out:** Khả năng truyền thông tin nhanh

**Ý nghĩa:**

- Người "nhanh nhạy" trong mạng
- Có khả năng tiếp cận mọi người nhanh chóng
- Phù hợp làm người điều phối hoặc truyền đạt thông tin khẩn cấp

**Kết quả Top 3:**

1. **Manager_Le:** 0.412
2. **Sales_Nguyen:** 0.382
3. **Warehouse_Dinh:** 0.326

---

### 4️⃣ Eigenvector Centrality (Độ trung tâm vector riêng)

**Khái niệm:** Đo lường uy tín dựa trên chất lượng kết nối, không chỉ số lượng

**Công thức:**

```
x(v) = (1/λ) Σ A(v,u) x(u)
```

Trong đó:

- A = ma trận kề
- λ = eigenvalue lớn nhất
- x = eigenvector tương ứng

**Triết lý:** "Bạn quan trọng nếu bạn kết nối với những người quan trọng"

**Ý nghĩa:**

- Đo lường "uy tín" và ảnh hưởng
- Kết nối với người có uy tín cao → bản thân cũng có uy tín cao
- Phản ánh vị trí trong hệ thống cấp bậc

**Kết quả Top 3:**

1. **Manager_Le:** 0.510 ⭐ UY TÍN CAO NHẤT
2. **Warehouse_Tran:** 0.409
3. **Warehouse_Dinh:** 0.409

---

## 🏆 KẾT QUẢ TỔNG HỢP

### Xếp hạng người quan trọng nhất

| Rank | Người tham gia  | Degree | Betweenness | Closeness | Eigenvector | **Tổng điểm** |
| ---- | --------------- | ------ | ----------- | --------- | ----------- | ------------- |
| 🥇 1 | **Manager_Le**  | 0.833  | **0.433**   | **0.412** | **0.510**   | **0.544**     |
| 🥈 2 | Warehouse_Dinh  | 0.833  | 0.150       | 0.326     | 0.409       | 0.408         |
| 🥉 3 | Warehouse_Tran  | 0.833  | 0.150       | 0.269     | 0.409       | 0.396         |
| 4    | Finance_Pham    | 0.667  | 0.056       | 0.273     | 0.362       | 0.313         |
| 5    | Sales_Vo        | 0.667  | 0.056       | 0.318     | 0.245       | 0.299         |
| 6    | Sales_Nguyen    | 0.500  | 0.056       | 0.382     | 0.245       | 0.270         |
| 7    | Logistics_Hoang | 0.333  | 0.000       | 0.200     | 0.393       | 0.202         |

### Công thức tính tổng điểm

```
Tổng điểm = Degree × 0.25 + Betweenness × 0.35 + Closeness × 0.20 + Eigenvector × 0.20
```

**Lý do phân bổ trọng số:**

- **Betweenness (35%):** Quan trọng nhất - người gác cổng kiểm soát luồng công việc
- **Degree (25%):** Số lượng kết nối phản ánh mức độ tham gia
- **Closeness (20%):** Khả năng điều phối và phản ứng nhanh
- **Eigenvector (20%):** Uy tín và ảnh hưởng trong tổ chức

---

## 🎯 PHÂN TÍCH VAI TRÒ

### 1. **Manager_Le** - NGƯỜI QUAN TRỌNG NHẤT 🏆

**Điểm mạnh:**

- ✅ **Gatekeeper số 1** (Betweenness 0.433) - Kiểm soát 43% luồng công việc
- ✅ **Hub trung tâm** (Degree 0.833) - Nhiều kết nối nhất
- ✅ **Coordinator hiệu quả** (Closeness 0.412) - Tiếp cận nhanh mọi người
- ✅ **Influencer** (Eigenvector 0.510) - Uy tín cao nhất

**Vai trò:**

- Điểm kết nối giữa Sales → Warehouse → Finance
- Duyệt tất cả các đơn hàng quan trọng
- Xử lý các trường hợp đặc biệt (special review)
- Liên hệ với supplier khi có vấn đề

**Rủi ro:**

- ⚠️ Single point of failure
- ⚠️ Nếu Manager_Le nghỉ việc → quy trình bị gián đoạn nghiêm trọng
- ⚠️ Bottleneck có thể xảy ra khi khối lượng công việc tăng

**Khuyến nghị:**

- 🔧 Cần training backup person
- 🔧 Phân quyền một số quyết định cho cấp dưới
- 🔧 Tạo quy trình tự động cho các trường hợp thông thường

---

### 2. **Warehouse Team** (Dinh & Tran) - Hub quan trọng

**Điểm mạnh:**

- Degree cao (0.833) - tham gia nhiều handover
- Eigenvector cao - kết nối với người quan trọng
- Cả 2 đều có Betweenness 0.150

**Vai trò:**

- Kiểm tra inventory
- Đóng gói sản phẩm
- Kết nối Sales → Manager và Finance → Logistics

**Đặc điểm:**

- Làm việc song song, hỗ trợ lẫn nhau
- Là điểm chuyển tiếp quan trọng trong quy trình

---

### 3. **Finance_Pham** - Specialist

**Vai trò:**

- Xử lý thanh toán
- Xử lý hoàn tiền (refund)
- Nhận việc từ Manager, giao cho Warehouse

**Đặc điểm:**

- Betweenness thấp (0.056) - chuyên môn hóa
- Closeness trung bình - không cần tiếp cận nhanh mọi người

---

### 4. **Sales Team** (Nguyen & Vo) - Front-line

**Vai trò:**

- Nhận đơn hàng từ khách hàng
- Liên hệ khách hàng khi cần
- Hủy đơn hàng

**Đặc điểm:**

- Sales_Nguyen có Closeness cao (0.382) - dễ tiếp cận
- Làm việc độc lập, ít phụ thuộc lẫn nhau

---

### 5. **Logistics_Hoang** - End-point

**Vai trò:**

- Giao hàng cho khách hàng
- Điểm kết thúc của quy trình

**Đặc điểm:**

- Betweenness = 0 - không nằm trên đường đi nào
- Out-Degree = 0 - chỉ nhận việc, không giao việc
- Eigenvector khá cao (0.393) - nhận việc từ Warehouse quan trọng

---

## 💡 INSIGHTS VÀ KHUYẾN NGHỊ

### 1. Rủi ro tập trung

**Vấn đề:**

- Manager_Le quá quan trọng (chiếm 43% kiểm soát)
- Nếu vắng mặt → quy trình tê liệt

**Giải pháp:**

```
✅ Đào tạo Deputy Manager
✅ Phân quyền duyệt đơn hàng thông thường cho Warehouse Manager
✅ Tạo escalation matrix rõ ràng
```

### 2. Tối ưu hóa quy trình

**Phát hiện:**

- Warehouse có vai trò trung gian cao
- Có thể tối ưu bằng cách:

```
Sales → Warehouse → Manager → Finance → Warehouse → Logistics
         ↓                      ↓
    (Check inventory)      (Payment)
```

**Đề xuất:**

```
✅ Tự động duyệt đơn hàng < $500
✅ Warehouse tự kiểm tra inventory và update system
✅ Finance tự động xử lý thanh toán online
```

### 3. Load balancing

**Vấn đề:**

- Manager xử lý quá nhiều handover
- Sales team có thể cân bằng tốt hơn

**Giải pháp:**

```
✅ Round-robin assignment cho Sales team
✅ Specialized teams (VIP orders, International orders)
✅ AI assistant để filter và route orders
```

### 4. Monitoring và KPIs

**Đề xuất theo dõi:**

```
📊 Handover frequency per person
📊 Average handover time
📊 Bottleneck detection (người có wait time cao nhất)
📊 Network density changes over time
```

---

## 🛠️ CÁC FILE TRONG DỰ ÁN

### 1. **handover_network_analysis.py**

- Code Python đầy đủ
- Tính toán 4 độ đo Centrality
- Tạo visualization và báo cáo

### 2. **handover_network_analysis.png**

- Visualization 4 đồ thị:
  - Main network (tổng hợp)
  - Degree Centrality
  - Betweenness Centrality
  - Top 5 ranking

### 3. **handover_analysis_report.xlsx**

- Sheet 1: Event Logs (39 events)
- Sheet 2: Handover Matrix (15 connections)
- Sheet 3: Centrality Summary (7 persons)

### 4. **handover_network_interactive.html**

- Interactive web visualization
- D3.js force-directed graph
- Tooltip với thông tin chi tiết
- Filter theo metric
- Responsive design

---

## 🚀 CÁCH SỬ DỤNG

### Chạy phân tích:

```bash
python handover_network_analysis.py
```

### Xem kết quả:

1. Mở `handover_network_analysis.png` để xem đồ thị
2. Mở `handover_analysis_report.xlsx` để xem dữ liệu chi tiết
3. Mở `handover_network_interactive.html` trong browser để tương tác

### Customize:

- Thay đổi data trong `create_mock_event_logs()`
- Điều chỉnh trọng số trong `identify_key_person()`
- Thêm metrics mới theo nhu cầu

---

## 📚 TÀI LIỆU THAM KHẢO

### Lý thuyết đồ thị:

- Newman, M. (2018). Networks. Oxford University Press.
- Barabási, A. L. (2016). Network Science. Cambridge University Press.

### Process Mining:

- van der Aalst, W. (2016). Process Mining: Data Science in Action.

### Social Network Analysis:

- Wasserman, S., & Faust, K. (1994). Social Network Analysis.

### Centrality Measures:

- Freeman, L. C. (1978). Centrality in social networks conceptual clarification.
- Borgatti, S. P. (2005). Centrality and network flow.

---

## 🎓 KẾT LUẬN

**Manager_Le** là người quan trọng nhất trong hệ thống với tổng điểm **0.544/1.0**, vượt xa người thứ 2 (0.408).

**4 lý do chính:**

1. ⭐ Gatekeeper số 1 - kiểm soát luồng công việc chính
2. ⭐ Hub trung tâm - nhiều kết nối nhất
3. ⭐ Coordinator - tiếp cận nhanh mọi người
4. ⭐ Influencer - uy tín và ảnh hưởng cao

**Hành động cần làm:**

- ✅ Đào tạo backup ngay lập tức
- ✅ Phân quyền để giảm tải
- ✅ Tạo quy trình dự phòng
- ✅ Monitor performance liên tục

---

**Tác giả:** minhnndev  
**Ngày:** 2026  
**Version:** 1.0

🔗 **Network Analysis** | 📊 **Process Mining** | 🎯 **Business Intelligence**
