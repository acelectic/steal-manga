"""Module providingFunction printing python version."""


HOST = 'https://www.manmirror.net'


def get_json(post_id: int, chapter: int, page: int) -> str:
    """function for get man mirror json suffer"""

    url = f'https://www.manmirror.net/test/{post_id}/{chapter}/{page}.json'

    print(url)
    return url
