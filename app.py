""" Main Module """
from man_mirror import ManMirror


if __name__ == "__main__":
    man_mirror = ManMirror()
    man_mirror.download_cartoons(10, max_chapter=10)
