from .scrapper import Scrapper


def get_image_data(link: str):
    """ Returns image data to bot """
    image = Scrapper(link, 'box')
    image_data = image.get_link_and_info()
    return image_data
