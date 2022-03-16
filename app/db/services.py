from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> List[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_delivered_messages_in_2015() -> List[User]:
    return list(User.objects.filter(message__sent__year=2015))


def get_actual_chats() -> List[Chat]:
    return list(Chat.objects.filter(message__sent__year__gte=2020).distinct())


def get_messages_contain_authors_first_name():
    return list(Message.objects.filter(text__contains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith="m") | Q(message__text__istartswith="a"),
    ))


def get_delivered_or_admin_messages() -> List[Message]:
    return list(Message.objects.filter(
        Q(delivered=True) | Q(user__username__startswith="admin"),
    ))


def get_messages_sent_by_first_name(first_name: str) -> List[Message]:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> List[User]:
    return User.objects.annotate(num_messages=Count('message')).order_by('-num_messages')[:3]


def get_last_5_messages_dicts() -> List[dict]:
    queryset = Message.objects.select_related("user").all().order_by("-sent")[:5]
    messages = []
    for message in queryset:
        messages.append({"from": message.user.username, "text": message.text})
    return messages


def get_chat_dicts() -> List[dict]:
    queryset = Chat.objects.prefetch_related('users')
    chats = []
    for chat in queryset:
        users = [user.username for user in chat.users.all()]
        chats.append({"id": chat.id, "title": chat.title, "users": users})
    return chats