from concurrent_lib import UNSPLASH_IMG_SCRAPER, CONCURRENT_IMG


def main():
    img = UNSPLASH_IMG_SCRAPER(15)
    con_obj = CONCURRENT_IMG(img.scrape_img())
    con_obj.concurrent_img_blur()


if __name__ == "__main__":
    main()
