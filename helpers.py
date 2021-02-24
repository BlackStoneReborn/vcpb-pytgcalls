import re
import random


def is_youtube(url):
    exp1 = r"(http|https)\:\/\/((www|m)\.|)youtu\.be\/.+"
    exp2 = r"(http|https)\:\/\/((www|m)\.|)youtube\.com\/watch.+"
    match = bool(re.match(exp1, url)) or bool(re.match(exp2, url))
    return match


def random_string():
    to_return = ""

    for i in range(10):
        to_return += random.choice(
            "A B C D E F G H I J K L M N O P Q R S T U V a b c d e f g h i j k l m n o p q r s t u v _".split()
        )

    return to_return
