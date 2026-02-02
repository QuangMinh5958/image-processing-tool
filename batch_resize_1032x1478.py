from pathlib import Path
from PIL import Image
import io
import time

# ===== PATH CONFIG =====
start_time = time.perf_counter()
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ===== IMAGE CONFIG =====
# -> tấm mail
TARGET_SIZE = (1032, 1478)
MAX_SIZE_KB = 270

# -> hình detail (kích thước)
# TARGET_SIZE = (900, 900)
# MAX_SIZE_KB = 80

MIN_QUALITY = 40
START_QUALITY = 90

# ===== PDF CONFIG =====
PDF_NAME = "result.pdf"


def compress_to_size(img, output_path):
    low, high = MIN_QUALITY, START_QUALITY
    best_data = None
    best_quality = MIN_QUALITY
    best_size = None

    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        img.save(buffer, "JPEG", quality=mid, subsampling=2)
        size_kb = buffer.tell() / 1024

        if size_kb <= MAX_SIZE_KB:
            best_data = buffer.getvalue()
            best_quality = mid
            best_size = size_kb
            low = mid + 1
        else:
            high = mid - 1

    output_path.write_bytes(best_data)
    return best_quality, best_size


def extract_index(path: Path):
    try:
        return int(path.stem.split("_")[0])
    except ValueError:
        return 999999


# ===============================
# 1️⃣ RESIZE + COMPRESS
# ===============================
print("🔄 Processing images...")

for img_path in INPUT_DIR.iterdir():
    if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue

    output_path = OUTPUT_DIR / f"{img_path.stem}.jpg"

    try:
        with Image.open(img_path) as img:
            img = img.convert("RGB")

            # ✅ ÉP KÍCH THƯỚC – KHÔNG CROP – CHO PHÉP MÉO
            img = img.resize(TARGET_SIZE, Image.LANCZOS)

            quality, size_kb = compress_to_size(img, output_path)

            print(
                f"{img_path.name} → {TARGET_SIZE[0]}x{TARGET_SIZE[1]}, "
                f"{size_kb:.1f}KB, quality={quality}"
            )

    except Exception as e:
        print(f"❌ Skip {img_path.name}: {e}")

print("✅ Image processing done!")


# ===============================
# 2️⃣ CREATE PDF
# ===============================
print("📄 Creating PDF...")

images = sorted(
    OUTPUT_DIR.glob("*.jpg"),
    key=extract_index
)

if not images:
    raise RuntimeError("❌ No images found to create PDF")

pdf_path = OUTPUT_DIR / PDF_NAME

with Image.open(images[0]) as first:
    pdf_pages = [
        Image.open(p).convert("RGB")
        for p in images[1:]
    ]

    first.save(
        pdf_path,
        save_all=True,
        append_images=pdf_pages
    )

print(f"✅ PDF created: {pdf_path}")
print(f"📄 Total pages: {len(images)}")
print("🎉 ALL DONE!")

elapsed = time.perf_counter() - start_time
print(f"⏱️ TOTAL RUN TIME: {elapsed:.2f} seconds")
