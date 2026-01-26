# Batch Image Resizer & Compressor (Pillow)

## 🎯 Mục tiêu

Script này dùng để xử lý **hàng loạt ảnh** trong một thư mục, đảm bảo:

- ✅ Kích thước ảnh đầu ra **chính xác 1032 × 1478 px**
- ✅ Dung lượng ảnh **< 500 KB**
- ✅ Không làm méo ảnh (giữ đúng tỉ lệ)
- ✅ Không chỉnh sửa file gốc

Công cụ phù hợp cho:

- Upload website
- Ảnh sản phẩm / ảnh form cố định size
- Automation nội bộ

---

## 🧰 Công nghệ sử dụng

- **Python 3**
- **Pillow (PIL)** – thư viện xử lý ảnh nhẹ, ổn định

Không cần:

- OpenCV
- Photoshop
- Tool ngoài

---

## 📂 Cấu trúc thư mục

project/
│
├── input/ # Chứa ảnh gốc
├── output/ # Chứa ảnh đã xử lý
└── script.py # File Python

## ⚙️ Cấu hình chính

```python
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
TARGET_WIDTH = 1032
TARGET_HEIGHT = 1478
MAX_SIZE_KB = 500
MIN_QUALITY = 40
```

TARGET_WIDTH: Chiều rộng ảnh output
TARGET_HEIGHT: Chiều cao ảnh output
MAX_SIZE_KB: Giới hạn dung lượng tối đa
MIN_QUALITY: Chất lượng thấp nhất cho phép

## 🧠 Logic xử lý tổng thể

Luồng xử lý:

- Đọc từng ảnh trong thư mục input
- Resize + crop ảnh về 1032×1478 (giữ tỉ lệ)
- Nén ảnh bằng JPG, giảm quality cho tới khi:
  - Dung lượng < 500KB
  - Hoặc chạm quality tối thiểu
- Lưu ảnh vào thư mục output

## Hướng dẫn

- B1: Di chuyển ảnh cần sửa vào thư mục input.
- B2: chạy file py cần dùng (1032x1478 hoặc 900x900).
- B3: Di chuyển các file trong mục output ra ngoài.
- B4: Xóa các file trong input, lập lại với các nhóm ảnh khác.

## flowchart TD

    A[Bắt đầu] --> B[Đọc folder input]
    B --> C{Có phải file ảnh?}
    C -- Không --> B
    C -- Có --> D[Resize ảnh 1032x1478]
    D --> E[Nén ảnh < 200KB]
    E --> F[Lưu ảnh vào folder output]
    F --> B
    B -->|Hết ảnh| G[Tạo PDF từ ảnh output]
    G --> H[Kết thúc]

## flowchart TD

    START([Start Script])

    START --> INIT[Load config<br/>TARGET_WIDTH<br/>TARGET_HEIGHT<br/>MAX_SIZE_KB]

    INIT --> MKDIR[Create output folder]

    MKDIR --> LOOP[Loop files in input folder]

    LOOP --> CHECK{File is JPG/PNG?}

    CHECK -- No --> LOOP

    CHECK -- Yes --> OPEN[Open image]

    OPEN --> RGB[Convert to RGB]

    RGB --> RESIZE[ImageOps.fit<br/>1032x1478<br/>LANCZOS]

    RESIZE --> COMPRESS[compress_to_size()]

    COMPRESS --> SAVEIMG[Save JPG to output]

    SAVEIMG --> LOOP

    LOOP -->|No more files| PDFSTART[Collect output images]

    PDFSTART --> SORT[Sort by numeric prefix<br/>1_, 2_, 3_...]

    SORT --> LOADPDF[Load images as RGB]

    LOADPDF --> SAVEPDF[Save as single PDF]

    SAVEPDF --> END([Done])

## flowchart TD

    A[Start compress_to_size] --> B[Set quality = 90]
    B --> C[Save image as JPG]
    C --> D[Check file size]
    D -->|<= MAX_SIZE_KB| E[Return quality & size]
    D -->|> MAX_SIZE_KB| F[Decrease quality by 5]
    F --> G{quality >= MIN_QUALITY?}
    G -- Yes --> C
    G -- No --> H[Return last result]
