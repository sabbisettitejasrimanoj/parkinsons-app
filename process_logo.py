from PIL import Image, ImageOps
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UPLOADS = PROJECT_ROOT / 'uploads'
OUT_DIR = PROJECT_ROOT / 'static' / 'images'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Supported image extensions
EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

# Find first image file in uploads
files = [p for p in UPLOADS.iterdir() if p.suffix.lower() in EXTS]

if not files:
    print('No image files found in uploads/. Please copy your logo into uploads/ and run this script again.')
    raise SystemExit(1)

src = files[0]
print(f'Processing logo from: {src.name}')

# Open and resize/crop to 200x200
with Image.open(src) as im:
    # Convert to RGBA to preserve transparency if present
    im = im.convert('RGBA')
    size = (200, 200)
    thumb = ImageOps.fit(im, size, Image.LANCZOS)

    out_path = OUT_DIR / 'logo.png'
    thumb.save(out_path, format='PNG', optimize=True)
    print(f'Saved resized logo to: {out_path}')
