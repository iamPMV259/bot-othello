## Đề tài: Bot Othello

Một trò chơi Othello được phát triển bằng Python và Pygame, cho phép người chơi đấu với máy tính sử dụng các thuật toán heuristic khác nhau.

## Thành viên

|     Sinh viên      |   MSSV    |
| ------------------ | --------- |
|   Phùng Minh Vũ    |  20235252 |
|   Trần Đức Thái    |  20235215 |
| Nguyễn Thanh Dương |  20235060 |

Nhóm 6 - lớp 157486 môn IT3160 - Nhập môn Trí tuệ nhân tạo


## Các kĩ thuật sử dụng

- Sử dụng Minimax Search, Alpha-Beta Prunning with iteractive deepening
- Nhiều chiến lược heuristic:
  - Đánh giá sự đối xứng của đồng xu (Coin Parity)
  - Chiến thuật chiếm góc (Corner Capturing)
  - Đánh giá độ ổn định (Stability)
  - Đánh giá khả năng di chuyển (Mobility)
- Đánh giá trọng số: 
  - Corners: 30
  - Stability: 25
  - Mobility: 5
  - Coin parity: 25


## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/bot-othello.git
cd bot-othello
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install uv
uv sync
```
or
```bash
python -m venv .venv
pip install -r requirements.txt
```

## Cách chơi

1. Chạy game:
```bash
source .venv/bin/activate
python3 src/main.py
```

2. Chọn bên chơi (Đen hoặc Trắng)
3. Chọn độ sâu tìm kiếm cho máy tính
4. Bắt đầu chơi!

### Luật chơi

- Người chơi lần lượt đặt quân vào các ô trống trên bàn cờ
- Mỗi nước đi phải lật ít nhất một quân của đối phương
- Quân bị lật sẽ đổi màu
- Người chơi có thể bỏ lượt nếu không có nước đi hợp lệ
- Game kết thúc khi không còn nước đi hợp lệ cho cả hai bên
- Người chơi có nhiều quân hơn sẽ thắng

## Cấu trúc dự án

```
bot-othello/
├── src/
│   ├── main.py           # Điểm khởi đầu của game
│   ├── othello.py        # Lớp chính quản lý game
│   ├── grid.py           # Quản lý bàn cờ và logic game
│   ├── tokens.py         # Quản lý quân cờ
│   ├── button.py         # Xử lý các nút trong giao diện
│   ├── color.py          # Định nghĩa màu sắc
│   ├── heuristics.py     # Các hàm đánh giá heuristic
│   └── computer_player.py # AI cho máy tính
└── README.md
```

