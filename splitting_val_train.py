from pathlib import Path
import shutil
import random

# ===== CONFIG =====
DATA_PATH = Path("/content/custom_data")
TRAIN_PCT = 0.9

IMAGES_PATH = DATA_PATH / "images"
LABELS_PATH = DATA_PATH / "labels"

BASE_PATH = Path("/content/data")
TRAIN_IMG_PATH = BASE_PATH / "train/images"
TRAIN_LABEL_PATH = BASE_PATH / "train/labels"
VAL_IMG_PATH = BASE_PATH / "validation/images"
VAL_LABEL_PATH = BASE_PATH / "validation/labels"

# ===== CREATE FOLDERS =====
for folder in [
    TRAIN_IMG_PATH,
    TRAIN_LABEL_PATH,
    VAL_IMG_PATH,
    VAL_LABEL_PATH
]:
    folder.mkdir(parents=True, exist_ok=True)

# ===== GET IMAGE FILES =====
valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

image_files = [
    f for f in IMAGES_PATH.iterdir()
    if f.is_file() and f.suffix.lower() in valid_extensions
]

random.shuffle(image_files)

# ===== TRAIN / VALIDATION SPLIT =====
train_count = int(len(image_files) * TRAIN_PCT)

train_files = image_files[:train_count]
val_files = image_files[train_count:]

# ===== COPY IMAGE + LABEL =====
def copy_image_and_label(files, img_dest, lbl_dest):
    labeled = 0
    empty = 0

    for img in files:
        # Copy image
        shutil.copy2(img, img_dest / img.name)

        # Exact matching label filename
        label = LABELS_PATH / f"{img.stem}.txt"

        if label.exists():
            shutil.copy2(label, lbl_dest / label.name)
            labeled += 1
        else:
            # Create empty YOLO label for background image
            (lbl_dest / f"{img.stem}.txt").touch()
            empty += 1

    return labeled, empty

# ===== COPY FILES =====
train_labeled, train_empty = copy_image_and_label(
    train_files,
    TRAIN_IMG_PATH,
    TRAIN_LABEL_PATH
)

val_labeled, val_empty = copy_image_and_label(
    val_files,
    VAL_IMG_PATH,
    VAL_LABEL_PATH
)

# ===== SUMMARY =====
print("Train/validation split complete!")
print()
print(f"Total images:      {len(image_files)}")
print(f"Training images:   {len(train_files)}")
print(f"Validation images: {len(val_files)}")
print()
print(f"Train labeled:     {train_labeled}")
print(f"Train empty:       {train_empty}")
print(f"Val labeled:       {val_labeled}")
print(f"Val empty:         {val_empty}")
