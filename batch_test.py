import os
from PIL import Image, ImageOps
import time

start_time = time.perf_counter()

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# ===== IMAGE CONFIG =====
TARGET_WIDTH = 1032
TARGET_HEIGHT = 1478
MAX_SIZE_KB = 270
MIN_QUALITY = 40

# ===== PDF CONFIG =====
PDF_NAME = "result.pdf"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def compress_to_size(img, output_path):
    """
    Nén ảnh JPG cho tới khi dung lượng <= MAX_SIZE_KB
    """
    quality = 90
    while quality >= MIN_QUALITY:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= MAX_SIZE_KB:
            return quality, size_kb
        quality -= 5
    return quality, size_kb


def extract_index(filename):
    """
    Lấy số thứ tự từ tên file:
    1_xxx.jpg -> 1
    """
    try:
        return int(filename.split("_")[0])
    except:
        return 999999


# ===============================
# 1️⃣ RESIZE + COMPRESS IMAGES
# ===============================
print("🔄 Processing images...")

for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.splitext(filename)[0] + ".jpg"
    )

    with Image.open(input_path) as img:
        img = img.convert("RGB")

        # Resize ép kích thước – không crop – cho phép méo
        img = img.resize(
            (TARGET_WIDTH, TARGET_HEIGHT),
            Image.LANCZOS
        )

        # Nén dung lượng
        quality, final_size = compress_to_size(img, output_path)
        print(
            f"{filename} → {TARGET_WIDTH}x{TARGET_HEIGHT}, "
            f"{final_size:.1f}KB, quality={quality}"
        )

print("✅ Image processing done!")


# ===============================
# 2️⃣ CREATE PDF FROM OUTPUT
# ===============================
print("📄 Creating PDF...")

images = [
    f for f in os.listdir(OUTPUT_FOLDER)
    if f.lower().endswith(".jpg")
]

images.sort(key=extract_index)

if not images:
    raise RuntimeError("❌ No images found to create PDF")

pdf_pages = []

for filename in images:
    path = os.path.join(OUTPUT_FOLDER, filename)
    img = Image.open(path).convert("RGB")
    pdf_pages.append(img)

pdf_path = os.path.join(OUTPUT_FOLDER, PDF_NAME)

pdf_pages[0].save(
    pdf_path,
    save_all=True,
    append_images=pdf_pages[1:]
)

print(f"✅ PDF created: {pdf_path}")
print(f"📄 Total pages: {len(pdf_pages)}")

print("🎉 ALL DONE!")

end_time = time.perf_counter()
elapsed = end_time - start_time

print(f"⏱️ TOTAL RUN TIME: {elapsed:.2f} seconds")