""" Main Module """
from man_mirror import ManMirror
from my_novel import MyNovel


if __name__ == "__main__":
    # man_mirror = ManMirror()
    # man_mirror.download_cartoons(10, max_chapter=10)

    my_novel = MyNovel()
    my_novel.download_cartoons('6yeQcr6kL14A96eUwKZA')
