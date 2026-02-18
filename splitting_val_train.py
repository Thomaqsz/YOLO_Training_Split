# --- Fixed train/validation label copy script ---

from pathlib import Path
import os
import shutil
import random
import argparse

# --------------------------
# Arguments
# --------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', help='Path to data folder containing image and label files', required=True)
parser.add_argument('--train_pct', help='Percentage of images to use for training (0-1)', default=0.8)
args = parser.parse_args()

data_path = args.datapath
train_percent = float(args.train_pct)

# --------------------------
# Paths
# --------------------------
input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

cwd = os.getcwd()
train_img_path = os.path.join(cwd, 'data/train/images')
train_txt_path = os.path.join(cwd, 'data/train/labels')
val_img_path = os.path.join(cwd, 'data/validation/images')
val_txt_path = os.path.join(cwd, 'data/validation/labels')

# Create folders if they don't exist
for p in [train_img_path, train_txt_path, val_img_path, val_txt_path]:
    os.makedirs(p, exist_ok=True)

# --------------------------
# Get all images
# --------------------------
img_file_list = list(Path(input_image_path).rglob('*'))
print(f'Total images found: {len(img_file_list)}')

# --------------------------
# Determine train/val split
# --------------------------
random.shuffle(img_file_list)
train_num = int(len(img_file_list) * train_percent)
train_imgs = img_file_list[:train_num]
val_imgs = img_file_list[train_num:]

# --------------------------
# Function to copy images and labels
# --------------------------
def copy_images_and_labels(img_list, img_dest, lbl_dest):
    for img_path in img_list:
        img_fn = img_path.name
        shutil.copy(img_path, os.path.join(img_dest, img_fn))

        # Handle labels with _rf suffix
        base_stem = img_path.stem.split('_rf')[0]
        for lbl_file in os.listdir(input_label_path):
            if lbl_file.startswith(base_stem) and lbl_file.endswith('.txt'):
                shutil.copy(os.path.join(input_label_path, lbl_file),
                            os.path.join(lbl_dest, lbl_file))

# --------------------------
# Copy train and validation sets
# --------------------------
copy_images_and_labels(train_imgs, train_img_path, train_txt_path)
copy_images_and_labels(val_imgs, val_img_path, val_txt_path)

print(f'Train images: {len(train_imgs)}, Validation images: {len(val_imgs)}')
print('Labels copied to train/val folders ✅')
