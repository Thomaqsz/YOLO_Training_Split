# train_val_split_fixed.py
from pathlib import Path
import random
import os
import sys
import shutil
import argparse

# -------------------------
# Parse user input
# -------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', required=True,
                    help='Path to data folder containing images and annotation files')
parser.add_argument('--train_pct', type=float, default=0.8,
                    help='Ratio of images to go to train folder (0.8 means 80% train, 20% val)')
args = parser.parse_args()

data_path = args.datapath
train_percent = args.train_pct
val_percent = 1 - train_percent

if not os.path.isdir(data_path):
    print(f"Directory {data_path} not found.")
    sys.exit(0)
if not 0.01 < train_percent < 0.99:
    print("train_pct must be between 0.01 and 0.99")
    sys.exit(0)

# -------------------------
# Paths
# -------------------------
input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

cwd = os.getcwd()
train_img_path = os.path.join(cwd, 'data/train/images')
train_txt_path = os.path.join(cwd, 'data/train/labels')
val_img_path = os.path.join(cwd, 'data/validation/images')
val_txt_path = os.path.join(cwd, 'data/validation/labels')

for dir_path in [train_img_path, train_txt_path, val_img_path, val_txt_path]:
    os.makedirs(dir_path, exist_ok=True)
    #print(f"Created folder at {dir_path}")

# -------------------------
# List all images
# -------------------------
img_file_list = [path for path in Path(input_image_path).rglob('*') if path.suffix.lower() in ['.jpg','.png']]
print(f"Number of image files: {len(img_file_list)}")

# Shuffle and split
random.shuffle(img_file_list)
train_num = int(len(img_file_list) * train_percent)
train_files = img_file_list[:train_num]
val_files = img_file_list[train_num:]

print(f"Images moving to train: {len(train_files)}")
print(f"Images moving to validation: {len(val_files)}")

# -------------------------
# Copy function
# -------------------------
def copy_images_and_labels(file_list, new_img_path, new_txt_path):
    for img_path in file_list:
        img_name = img_path.name
        shutil.copy(img_path, os.path.join(new_img_path, img_name))

        base_stem = img_path.stem.split('_rf')[0]  # handle _rf suffix
        # Copy any label file that starts with base_stem
        for lbl_file in os.listdir(input_label_path):
            if lbl_file.startswith(base_stem) and lbl_file.endswith('.txt'):
                shutil.copy(os.path.join(input_label_path, lbl_file),
                            os.path.join(new_txt_path, lbl_file))

# -------------------------
# Copy train and val
# -------------------------
copy_images_and_labels(train_files, train_img_path, train_txt_path)
copy_images_and_labels(val_files, val_img_path, val_txt_path)

print("✅ Images and labels synced successfully!")
