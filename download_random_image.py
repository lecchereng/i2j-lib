import requests
import sys

def download_random_image(filename: str):
    url = "https://picsum.photos/300/200"
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved as: {filename}")
    except requests.RequestException as e:
        print(f"❌ Failed to download image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_random_image.py <filename>")
    else:
        filename = sys.argv[1]
        download_random_image(filename)
