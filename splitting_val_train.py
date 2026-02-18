# splitting_val_train_fixed_v2.py

from pathlib import Path
import random
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--datapath', required=True, help='Path to data folder containing images and labels')
parser.add_argument('--train_pct', default=0.8, type=float, help='Percentage of images for training')
args = parser.parse_args()

data_path = args.datapath
train_pct = args.train_pct

# Paths
input_images = Path(data_path) / "images"
input_labels = Path(data_path) / "labels"

train_images = Path("data/train/images")
train_labels = Path("data/train/labels")
val_images = Path("data/validation/images")
val_labels = Path("data/validation/labels")

# Make folders if they don't exist
for folder in [train_images, train_labels, val_images, val_labels]:
    folder.mkdir(parents=True, exist_ok=True)

# Get all image files
image_files = list(input_images.glob("*"))
random.shuffle(image_files)

train_count = int(len(image_files) * train_pct)

for idx, img_path in enumerate(image_files):
    # Find label file that contains image stem
    matching_labels = list(input_labels.glob(f"{img_path.stem}*.txt"))
    
    if idx < train_count:
        shutil.copy(img_path, train_images / img_path.name)
        for label_file in matching_labels:
            shutil.copy(label_file, train_labels / label_file.name)
    else:
        shutil.copy(img_path, val_images / img_path.name)
        for label_file in matching_labels:
            shutil.copy(label_file, val_labels / label_file.name)

print("Train/validation split complete!")
print(f"Train images: {len(list(train_images.glob('*')))}")
print(f"Validation images: {len(list(val_images.glob('*')))}")
print(f"Train labels: {len(list(train_labels.glob('*')))}")
print(f"Validation labels: {len(list(val_labels.glob('*')))}")
