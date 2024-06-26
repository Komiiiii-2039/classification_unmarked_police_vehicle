import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def save_image(image_url, save_directory):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        # 画像のファイル名を取得
        image_name = os.path.basename(urlparse(image_url).path)
        if not image_name:
            image_name = 'default_image_name.jpg'

        # 画像を保存
        with open(os.path.join(save_directory, image_name), 'wb') as file:
            file.write(response.content)
        print(f"Saved image: {image_url}")

    except Exception as e:
        print(f"Failed to save image {image_url}: {e}")

def scrape_images_from_url(url, save_directory, base_url, depth=0, max_depth=2):
    if depth > max_depth:
        return

    if url in visited_urls:
        return

    visited_urls.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 画像リンクを収集
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                save_image(img_url, save_directory)

        # 再帰的にリンクを収集して画像を保存
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                next_url = urljoin(url, href)
                next_url_parsed = urlparse(next_url)
                base_url_parsed = urlparse(base_url)

                # 同一ドメインかつ開始URLのパスよりも上位でない場合にのみ遷移する
                if (next_url_parsed.netloc == base_url_parsed.netloc and 
                    next_url_parsed.path.startswith(base_url_parsed.path)):
                    scrape_images_from_url(next_url, save_directory, base_url, depth + 1, max_depth)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

if __name__ == "__main__":
    start_url = "https://policecar.nomaki.jp/fukumen/crown/"
    save_directory = "./images/unmarked_crown"  # ここに保存先ディレクトリを指定

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    scrape_images_from_url(start_url, save_directory, start_url)
