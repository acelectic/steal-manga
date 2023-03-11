""" Main Module """
from man_mirror import ManMirror
from my_novel import MyNovel


if __name__ == "__main__":
    # man_mirror = ManMirror()
    # man_mirror.download_cartoons(10, max_chapter=10)

    my_novel_cartoons = [
        # ['Against the Gods - อสูรพลิกฟ้า', '6EvFPzipwmnKxlZMqhjs', 423],
        ['Cultivator vs Superhero', '6yeQcr6kL14A96eUwKZA', 250],
        # ['Tales of Demon and Gods', 'E8XDEk8Dv9vbchSGtF5n', 419],
    ]
    my_novel = MyNovel()
    for cartoon_name, cartoon_id, latest_chapter in my_novel_cartoons:
        print(
            f'cartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        my_novel.download_cartoons(cartoon_id, start_ep_index=latest_chapter)
