# --- Colab-ready YOLO Train/Val Split Script ---
from pathlib import Path
import shutil
import random
import os

# ===== CONFIG =====
DATA_PATH = Path("/content/custom_data")  # path to your dataset folder
TRAIN_PCT = 0.9                           # ratio of images for training

IMAGES_PATH = DATA_PATH / "images"
LABELS_PATH = DATA_PATH / "labels"

# Where to copy the split files
BASE_PATH = Path("/content/data")
TRAIN_IMG_PATH = BASE_PATH / "train/images"
TRAIN_LABEL_PATH = BASE_PATH / "train/labels"
VAL_IMG_PATH = BASE_PATH / "validation/images"
VAL_LABEL_PATH = BASE_PATH / "validation/labels"

# ===== CREATE FOLDERS =====
for folder in [TRAIN_IMG_PATH, TRAIN_LABEL_PATH, VAL_IMG_PATH, VAL_LABEL_PATH]:
    folder.mkdir(parents=True, exist_ok=True)

# ===== RENAME LABEL FILES TO MATCH IMAGE STEM =====
print("Renaming labels to match images...")
for lbl in LABELS_PATH.glob("*"):
    # keep only the part before '.rf.' to match image stem
    new_name = lbl.stem.split(".rf.")[0] + ".txt"
    lbl.rename(LABELS_PATH / new_name)
print("Label renaming complete ✅\n")

# ===== GET LIST OF IMAGES =====
image_files = list(IMAGES_PATH.glob("*"))
random.shuffle(image_files)

train_count = int(len(image_files) * TRAIN_PCT)
val_count = len(image_files) - train_count

train_files = image_files[:train_count]
val_files = image_files[train_count:]

# ===== FUNCTION TO COPY IMAGE + LABEL =====
def copy_image_and_label(files, img_dest, lbl_dest):
    count = 0
    for img in files:
        # Copy image
        shutil.copy(img, img_dest / img.name)

        # Construct label filename
        label_file = LABELS_PATH / (img.stem.split(".rf.")[0] + ".txt")
        if label_file.exists():
            shutil.copy(label_file, lbl_dest / label_file.name)
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
