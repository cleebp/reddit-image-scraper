import os
from time import sleep
import re
from urllib.request import urlretrieve, HTTPError

from selenium import webdriver

from config import *


def initialize():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    dir_path = os.path.join(os.getcwd(), 'scrapes/')
    init_folders(dir_path)

    return driver, dir_path


def init_folders(dir_path):
    _create_if_not_exists(dir_path)
    for path in URLS:
        sub_path = dir_path + path.split('/')[-1]
        _create_if_not_exists(sub_path)
        _create_if_not_exists(sub_path + '/img/')
        _create_if_not_exists(sub_path + '/mp4/')


def scrape(driver, dir_path):
    first_pass = True
    for path in URLS:
        print(f'=== Beginning scrape of {path} ===')
        url = str(path) + TOP_BASE + TOP_YEAR  # TODO: grab TOP_ALL/MONTH/etc from command line arg
        driver.get(url)
        sleep(SCRAPE_BUFFER)

        # turn off auto slides
        if first_pass:
            driver.find_element_by_id('autoNextSlide').click()
            first_pass = False
            sleep(SCRAPE_BUFFER)

        img_path = dir_path + path.split('/')[-1] + '/img/'
        gif_path = dir_path + path.split('/')[-1] + '/mp4/'

        for i in range(SCRAPE_ITERATIONS):
            html = driver.execute_script("return document.body.innerHTML")
            img_match = re.search('url\\(&quot;(.*?)&quot;', html)
            gif_match = re.search('src=\\"(.*?)\\.mp4', html)
            if img_match:
                _save_image(img_match, img_path)
            elif gif_match:
                _save_gif(gif_match, gif_path)
            else:
                print('Error finding image/gif, skipping...')

            _next_image()

        print('=== done scrapin ===\n')
        sleep(1)


def _create_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def _save_image(img_match, img_path):
    if img_match:
        url = img_match.group(1)
        name = url[re.search('.*//.*/(.*?)', url).regs[0][1]:]
        full_path = str(img_path) + str(name)
        if not os.path.exists(full_path) and name:
            try:
                urlretrieve(url, full_path)
                print(f'New image found, saving image {name}.')
            except HTTPError:
                print('Image not found... skipping...')
        elif name:
            print(f'Skipping image {name}...')


def _save_gif(gif_match, gif_path):
    url = gif_match.group(0)
    name = url.split('/')[-1]
    if 'gfycat' in url:
        url = 'https://giant.gfycat.com/' + name
    elif 'imgur' in url:
        url = 'https://i.imgur.com/' + name
    else:
        print('Error saving gif, skipping...')
        return

    full_path = str(gif_path) + str(name)
    if not os.path.exists(full_path) and name:
        try:
            urlretrieve(url, full_path)
            print(f'New gif found, saving gif {name}.')
        except HTTPError:
            print("Gif not found, skipping gif...")
    elif name:
        print(f'Skipping gif {name}...')


def _next_image():
    driver.find_element_by_id('nextButton').click()
    sleep(SCRAPE_BUFFER)


if __name__ == '__main__':
    driver, dir_path = initialize()
    scrape(driver, dir_path)
    driver.close()
    driver.quit()
