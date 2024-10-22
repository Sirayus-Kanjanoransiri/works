import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import base64

def create_download_folder(branch_folder, index):
    download_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Image Data for Training", "celebrities", f"{index}_{branch_folder}")
    os.makedirs(download_folder, exist_ok=True)
    return download_folder

def is_valid_image(url):
    return not any(keyword in url for keyword in ["logo", "favicon", "icon", "site", "thumbnail", "16x16"])

def download_image(img_url, index, download_folder):
    try:
        random_second = random.randint(1, 3)  # กำหนด Cooldown
        if img_url.startswith('data:image/'):
            header, encoded = img_url.split(',', 1)
            data = base64.b64decode(encoded)
            if len(data) > 5120:  # Check size more than 5KB
                filename = f'{index + 1}.jpg'
                with open(os.path.join(download_folder, filename), 'wb') as f:
                    f.write(data)
                    print("break for: ", random_second, " Second")
                    time.sleep(random_second)
                print(f'Downloaded {filename} from Base64')
                return True
            else:
                print(f'Skipped small Base64 image')
        elif img_url.startswith(('http://', 'https://')):
            response = requests.get(img_url)
            if response.status_code == 200 and len(response.content) > 5120:  # Check size more than 5KB
                filename = f'{index + 1}.jpg'
                with open(os.path.join(download_folder, filename), 'wb') as f:
                    f.write(response.content)
                    print("break for: ", random_second, " Second")
                    time.sleep(random_second)
                print(f'Downloaded {filename}')
                return True
            else:
                print(f'Skipped small image or failed request')
    except Exception as e:
        print(f'Could not download image_{index + 1}: {e}')
    return False

def main():
    index = 1  # ตัวเลขนำหน้าเริ่มต้น
    while True:  # Start an infinite loop
        branch_folder = input("Folder Name: ")
        download_folder = create_download_folder(branch_folder, index)
        driver = webdriver.Chrome()
        search_query = input("Image you want to download: ")
        number_of_images = int(input("Number of images to download: "))

        url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query}"
        driver.get(url)
        time.sleep(2)

        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        images = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

        filtered_image_urls = [url for url in image_urls if is_valid_image(url)]

        downloaded_count = 0
        downloaded_urls = set()  # Set to keep track of downloaded URLs

        for img_url in filtered_image_urls:
            if downloaded_count >= number_of_images:
                break
            if img_url not in downloaded_urls:  # Check if already downloaded
                if download_image(img_url, downloaded_count, download_folder):
                    downloaded_urls.add(img_url)  # Add URL to the set if downloaded
                    downloaded_count += 1

        driver.quit()

        # Ask if the user wants to repeat the process
        repeat = input("Do you want to download images again? (0/1): ").strip().lower()
        if repeat != '1':
            index += 1  # เพิ่มค่าตัวนับเมื่อทำการดาวน์โหลดใหม่
        else:
            break  # Exit the loop

if __name__ == "__main__":
    main()
