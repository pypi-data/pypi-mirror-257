from .define import bot, CHAT_ID


def send_photo(file_path: str, caption: str):
    photo = open(file_path, 'rb')
    bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)


if __name__ == "__main__":
    send_photo('/home/bigzhu/Pictures/00006.jpeg', 'test')
