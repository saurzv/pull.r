import requests
from bs4 import BeautifulSoup


class Scrapper:
    """ Scrape the web page for required information """

    def __init__(self, url: str, classid: str):
        self.url = url
        self.classid = classid

    def get_link_and_info(self):
        """ Return link and description for xkcd images """

        image_data = []

        rsp = requests.get(self.url)
        soup = BeautifulSoup(rsp.text, 'html.parser')
        links = soup.findAll('div', class_=self.classid)

        for link in links:
            image_tag = link.findChildren('img')
            if len(image_tag):
                image_data.append('https:' + image_tag[0]["src"])
                image_data.append(image_tag[0]["alt"])
                image_data.append(image_tag[0]["title"])
                image_data.append(rsp.url)
                return image_data
