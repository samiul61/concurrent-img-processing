import requests
from bs4 import BeautifulSoup
import concurrent.futures
from PIL import Image, ImageFilter



class UNSPLASH_IMG_SCRAPER:
    URL = "https://unsplash.com/"
    HTML_ELEMENT = "figure"

    def __init__(self, element_amount):
        self.element_amount = element_amount

    # takes url creates an beautiful soup obj and outputs that object with identified element amount.
    def scrape_img(self):
        soup = BeautifulSoup(requests.get(self.URL, allow_redirects=True).content, "html.parser")
        figures = soup.find_all(self.HTML_ELEMENT)[0:self.element_amount]
        return list(map(lambda figure: figure.div.div.find_all("div", {"class": "MorZF"})[0].div.img["src"].__str__(),
                        figures))



class CONCURRENT_IMG:
    SIZE = (1200, 1200)
    IMG_NAME = []

    def __init__(self, img_urls):
        self.img_urls = img_urls

    # takes an img url in downloads that img.
    def download_img(self, img_url):
        img_bytes = requests.get(img_url).content
        img_name = img_url.split("/")[-1]
        img_name = f"{img_name}.jpg"
        self.IMG_NAME.append(img_name)
        with open("img/" + img_name, "wb") as img_file:
            img_file.write(img_bytes)
            print("downloaded")

    # takes a name of an img as an argument, looks for that in img folder, then blurs the img and saves in processed folder
    def blur_img(self, img_name):
        img = Image.open("img/" + img_name)
        img = img.filter(ImageFilter.GaussianBlur(15))
        img.thumbnail(self.SIZE)
        img.save(f"processed/{img_name}")
        print("processed")

    def concurrent_img_blur(self):
        # downloads images using multi-threading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.download_img, self.img_urls)

        # processes images using multi-processing
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.blur_img, self.IMG_NAME)