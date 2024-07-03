import os
import glob
from PIL import Image
import torch
from torchvision import transforms

# クラスと設定
classes = ["crown_normal", "crown_police"]
num_classes = len(classes)
image_size = 128

# データセットのディレクトリ
datadir = "./images"

# 基本の画像の前処理
base_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# データとラベルを格納するリスト
data = []
labels = []

# データセットの作成
for index, classlabel in enumerate(classes):
    image_dir = os.path.join(datadir, classlabel)
    files = glob.glob(os.path.join(image_dir, "*"))
    if len(files) == 0:
        print(f"No files in {image_dir}")
        continue
    for file in files:
        image = Image.open(file)
        image = image.convert("RGB")

        # オリジナル画像
        data.append(base_transform(image))
        labels.append(index)

        # 回転
        for angle in range(-20, 21, 5):
            img_r = image.rotate(angle)
            data.append(base_transform(img_r))
            labels.append(index)

        # 反転
        img_trans = image.transpose(Image.FLIP_LEFT_RIGHT)
        data.append(base_transform(img_trans))
        labels.append(index)

print(f"Original and augmented dataset created.")

# テンソルに変換
data = torch.stack(data)
labels = torch.tensor(labels)

# 各クラスのデータ数を表示
for label in range(num_classes):
    print(f"{classes[label]}: {torch.sum(labels == label)}")

# データセットを保存
torch.save((data, labels), 'crown.pt')
print("Dataset augmented and saved successfully.")