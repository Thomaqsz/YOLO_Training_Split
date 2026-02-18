# --- Robust YOLO Train/Val Split Script ---
from pathlib import Path
import shutil
import random
import os

# ===== CONFIG =====
DATA_PATH = Path("/content/custom_data")  # path to dataset folder
TRAIN_PCT = 0.9

IMAGES_PATH = DATA_PATH / "images"
LABELS_PATH = DATA_PATH / "labels"

BASE_PATH = Path("/content/data")
TRAIN_IMG_PATH = BASE_PATH / "train/images"
TRAIN_LABEL_PATH = BASE_PATH / "train/labels"
VAL_IMG_PATH = BASE_PATH / "validation/images"
VAL_LABEL_PATH = BASE_PATH / "validation/labels"

for folder in [TRAIN_IMG_PATH, TRAIN_LABEL_PATH, VAL_IMG_PATH, VAL_LABEL_PATH]:
    folder.mkdir(parents=True, exist_ok=True)

# ===== GET LIST OF LABELS =====
label_files = {lbl.stem: lbl for lbl in LABELS_PATH.glob("*.txt")}  # dict: stem -> file
print(f"Found {len(label_files)} label files")

# ===== GET LIST OF IMAGES =====
image_files = list(IMAGES_PATH.glob("*"))
random.shuffle(image_files)

train_count = int(len(image_files) * TRAIN_PCT)
train_files = image_files[:train_count]
val_files = image_files[train_count:]

# ===== FUNCTION TO COPY IMAGE + LABEL =====
def copy_image_and_label(files, img_dest, lbl_dest):
    count = 0
    for img in files:
        shutil.copy(img, img_dest / img.name)

        # Find matching label
        matched_label = None
        for lbl_stem, lbl_path in label_files.items():
            if img.stem.startswith(lbl_stem):
                matched_label = lbl_path
                break

        if matched_label:
            shutil.copy(matched_label, lbl_dest / matched_label.name)
            count += 1
    return count

# ===== COPY FILES =====
train_labels_count = copy_image_and_label(train_files, TRAIN_IMG_PATH, TRAIN_LABEL_PATH)
val_labels_count = copy_image_and_label(val_files, VAL_IMG_PATH, VAL_LABEL_PATH)

# ===== SUMMARY =====
print("Train/validation split complete!")
print(f"Train images: {len(train_files)}")
print(f"Validation images: {len(val_files)}")
print(f"Train labels: {train_labels_count}")
print(f"Validation labels: {val_labels_count}")
