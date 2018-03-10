from app.models import UserProfile, SwipeAction, Event
from loremipsum import get_sentence, get_paragraph


def get_word():
    return get_sentence().split()[0]


def create_user_profile():
    user_profile = UserProfile(
        first_name=get_word(),
        last_name=get_word())
    user_profile.save()
    return user_profile


def create_event(is_active=True):
    event = Event(
        name='%s Event' % get_word(),
        is_active=is_active)
    event.save()
    return event
