import os
import shutil
import random
import argparse

parser = argparse.ArgumentParser(description="train/test split script")
parser.add_argument("--data_dir", type=str, required=True, help="원본 데이터 폴더 경로(PetImages 폴더)")
args = parser.parse_args()

original_dir = args.data_dir

base_dir = "dataset"
train_dir = os.path.join(base_dir, "train")
test_dir = os.path.join(base_dir, "test")

categories = ["Dog", "Cat"]

split_ratio = 0.8

for category in categories:
    os.makedirs(os.path.join(train_dir, category.lower()), exist_ok=True)
    os.makedirs(os.path.join(test_dir, category.lower()), exist_ok=True)

# 폴더별 개수 비교하고 필요한 경우 downsampling
img_counts = {}
for category in categories:
    source = os.path.join(original_dir, category)
    if not os.path.exists(source):
        print("{source} 경로를 찾을 수 없습니다.")
        continue
    
    images = os.listdir(source)
    images = [img for img in images if img.endswith(('.jpg', '.png', '.jpeg'))]

    img_counts[category] = len(images)
    print(f"{category} 폴더의 총 이미지 개수: {len(images)}")

min_img = min(img_counts.values())
if img_counts["Dog"] == img_counts["Cat"]:
    print(f"폴더별 이미지 개수 같음")
else:
    print(f"모든 클래스에 대해 {min_img}개로 downsampling 진행")

for category in categories:
    source = os.path.join(original_dir, category)
    images = os.listdir(source) # listdir - 파일 목록 가져오기
    images = [img for img in images if img.endswith(('.jpg', '.png', '.jpeg'))]    

    valid_img = [img for img in images if os.path.exists(os.path.join(source, img))]

    # downsampling
    if img_counts["Dog"] != img_counts["Cat"] and len(valid_images) > min_img:
        valid_images = random.sample(valid_images, min_img)
        print(f"{category} 폴더 -> {min_img}개로 Downsampling")

    random.shuffle(valid_img)

    split_idx = int(len(valid_img) * split_ratio)
    train_img = valid_img[:split_idx]
    test_img = valid_img[split_idx]

    def move_img(src, dst):
        base, ext = os.path.splitext(dst)
        count = 1
        while os.path.exists(dst):
            dst = f"{base}_{count}{ext}"
            count += 1
        shutil.move(src, dst)

    for img in train_img:
        src = os.path.join(source, img)
        dst = os.path.join(train_dir, category.lower(), img)
        if os.path.exists(src):
            move_img(src, dst)
        else:
            print(f"파일이 존재하지 않음 (train): {src}")

    for img in test_img:
        src = os.path.join(source, img)
        dst = os.path.join(test_dir, category.lower(), img)
        if os.path.exists(src):
            move_img(src, dst)
        else:
            print(f"파일이 존재하지 않음 (test): {src}")

print("데이터 분할 완료!!")



    