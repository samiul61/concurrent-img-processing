import requests
from bs4 import BeautifulSoup
import concurrent.futures
from PIL import Image, ImageFilter

URL = "https://unsplash.com/"
ELEMENTS_AMOUNT = 1
HTML_ELEMENT = "figure"
SIZE = (1200, 1200)


# takes url creates an beautiful soup obj and outputs that object with identified element amount.
def soup_obj_create():
    soup = BeautifulSoup(requests.get(URL, allow_redirects=True).content, "html.parser")
    return soup.find_all(HTML_ELEMENT)[0:ELEMENTS_AMOUNT]


# takes an img url in downloads that img.
def download_img(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split("/")[-1]
    img_name = f"{img_name}.jpg"
    with open("img/" + img_name, "wb") as img_file:
        img_file.write(img_bytes)
        print("downloaded")
    return img_name


# takes a name of an img as an argument, looks for that in img folder, then blurs the img and saves in processed folder
def blur_img(img_name):
    img = Image.open("img/" + img_name)
    img = img.filter(ImageFilter.GaussianBlur(15))
    img.thumbnail(SIZE)
    img.save(f"processed/{img_name}")
    print("processed")


def main():
    figures = soup_obj_create()

    img_urls = list(map(lambda figure: figure.div.div.find_all("div", {"class": "MorZF"})[0].div.img["src"].__str__(),
                        figures))

    # downloads images using multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_name = executor.map(download_img, img_urls)

    # processes images using multi-processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(blur_img, image_name)


if __name__ == "__main__":
    main()
