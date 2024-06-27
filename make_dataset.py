import os
import glob
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
from sklearn.model_selection import train_test_split

# クラスと設定
classes = ["normal", "unmarked_crown"]
num_classes = len(classes)
image_size = 128

# データセットのディレクトリ
datadir = "./images"

# 画像の前処理
transform = transforms.Compose([
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
    if len(files) == 0 :
        print(f"No files in {image_dir}")
        continue
    for file in files:
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))

        # オリジナル画像
        data.append(transform(image))
        labels.append(index)

        # 回転
        for angle in range(-20, 20, 5):
            img_r = image.rotate(angle)
            data.append(transform(img_r))
            labels.append(index)

        # 反転
        img_trans = image.transpose(Image.FLIP_LEFT_RIGHT)
        data.append(transform(img_trans))
        labels.append(index)
    print(f"Create dataset for {classlabel}")

# テンソルに変換
data = torch.stack(data)
labels = torch.tensor(labels)

# データセットを保存
torch.save((data, labels), 'crown.pt')