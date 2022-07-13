from .scrapper import Scrapper


def get_image_data(message: str):
    """ Returns image data to bot """
    img_link = ''
    if(message == '-x frontpg'):
        img_link = 'https://xkcd.com'
    elif(message == '-x random'):
        img_link = 'https://c.xkcd.com/random/comic/'
    else:
        return -1

    image = Scrapper(img_link, 'box')
    image_data = image.get_link_and_info()
    return image_data
