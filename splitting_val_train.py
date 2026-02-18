from pathlib import Path
import shutil
import random

# Paths
data_path = Path("/content/custom_data")
images_path = data_path / "images"
labels_path = data_path / "labels"

train_images_path = Path("/content/data/train/images")
train_labels_path = Path("/content/data/train/labels")
val_images_path = Path("/content/data/validation/images")
val_labels_path = Path("/content/data/validation/labels")

# Make folders AAAAA
for folder in [train_images_path, train_labels_path, val_images_path, val_labels_path]:
    folder.mkdir(parents=True, exist_ok=True)

# Get all images
all_images = list(images_path.glob("*"))
random.shuffle(all_images)

train_ratio = 0.9
train_count = int(len(all_images) * train_ratio)

# Get all label files recursively
all_labels = list(labels_path.rglob("*.txt"))

def find_labels_for_image(image_stem):
    # Return all labels that start with the image stem
    return [lbl for lbl in all_labels if lbl.name.startswith(image_stem)]

# Split and copy
for i, img_file in enumerate(all_images):
    labels_for_img = find_labels_for_image(img_file.stem)
    
    if i < train_count:
        shutil.copy(img_file, train_images_path / img_file.name)
        for lbl in labels_for_img:
            shutil.copy(lbl, train_labels_path / lbl.name)
    else:
        shutil.copy(img_file, val_images_path / img_file.name)
        for lbl in labels_for_img:
            shutil.copy(lbl, val_labels_path / lbl.name)

print("Train/validation split complete!")
print(f"Train images: {len(list(train_images_path.glob('*')))}")
print(f"Validation images: {len(list(val_images_path.glob('*')))}")
print(f"Train labels: {len(list(train_labels_path.glob('*')))}")
print(f"Validation labels: {len(list(val_labels_path.glob('*')))}")
