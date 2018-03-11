from app.models import Image
from loremipsum import get_sentence


def get_word():
    return get_sentence().split()[0]


def create_image():
    image = Image(name=get_word())
    image.save()
    return image
