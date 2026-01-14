# XSMB Daily Dashboard

> 📊 Dashboard thống kê Xổ Số Miền Bắc (XSMB) – tự động cập nhật mỗi ngày, hiển thị trực quan trên GitHub Pages.

![status](https://img.shields.io/badge/status-active-brightgreen)
![update](https://img.shields.io/badge/update-daily-blue)
![pages](https://img.shields.io/badge/GitHub%20Pages-live-success)

---

## 🌐 Live Website
👉 **https://anhducati.github.io/USA-lottery/**

Trang web hiển thị:
- Kết quả XSMB mới nhất
- Lịch 7 ngày gần nhất (đầy đủ tất cả giải)
- Top 10 số lâu chưa về
- Top 10 số xuất hiện nhiều nhất (30 ngày)
- Biểu đồ thống kê (line, heatmap, distribution…)

---

## ✨ Tính năng chính

- 🔄 **Tự động cập nhật mỗi ngày**
- ⏰ Canh giờ kết quả XSMB (18:30 VN, có retry khi trễ)
- 🌈 Dashboard tông sáng, viền LED 7 màu
- 🔴 LED cảnh báo khi chưa có kết quả hôm nay
- 📱 Tối ưu giao diện mobile
- 📊 Biểu đồ sinh tự động bằng Python
- 🤖 Hoàn toàn chạy bằng **GitHub Actions** (không cần server riêng)

---

## 🗂️ Cấu trúc dữ liệu

### 📄 JSON Data
| File | Mô tả |
|----|----|
| `data/xsmb.json` | Toàn bộ kết quả XSMB (raw data) |
| `data/last7.json` | Kết quả 7 ngày gần nhất (full giải) |
| `data/top10_delta.json` | Top 10 số lâu chưa về |
| `data/top10_30d.json` | Top 10 số xuất hiện nhiều nhất (30 ngày) |
| `data/site_meta.json` | Thông tin cập nhật (thời gian, commit, trạng thái) |

### 🖼️ Charts & Images
