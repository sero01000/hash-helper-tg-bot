from name_that_hash import runner
from hashlib import md5
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import base64


def prepare_text(text):
    text = text.replace("\n", " ")
    words = text.split(' ')
    return words


def prepare_detect(words_to_check):
    detect = detect_hashes(words_to_check)
    detect = list(dict.fromkeys(detect))
    detect = [i for i in detect if i is not None]
    answer = "\n\n".join(detect)
    return answer


def prepare_words(words):
    words = list(dict.fromkeys(words))
    words_to_check = []

    for word in words:
        if is_hex(word):
            words_to_check.append(word)
        else:
            b64_word = decode_base64(word)
            if b64_word is not None:
                words_to_check.append(b64_word)
            if len(word)>4:#smallest hash lenth
                words_to_check.append(word)
    return words_to_check


def detect_hashes(hashes, popular_only=False):
    output = runner.api_return_hashes_as_dict(hashes, {"popular_only": popular_only})

    result = []
    for key in output:
        if len(output[key]) > 0:
            detect_str = key
            for detect in output[key]:
                if detect['hashcat'] is not None:
                    detect_str += f"\n[+] {detect['name']} | hashcat: {detect['hashcat']}"
            if detect_str == key:
                result.append(None)
            else:
                result.append(detect_str)
        else:
            result.append(None)
    return result


def prepare_querry(title, message, img):
    id: str = md5(message.encode()).hexdigest()
    statistic = InlineQueryResultArticle(

        id=id,

        title=title,

        input_message_content=InputTextMessageContent(message),

        thumb_url=img,

        description=message
    )
    return statistic


def decode_base64(sb):
    try:
        b64_dec = base64.b64decode(sb).hex()
        return b64_dec
    except Exception as e :
        return None


def is_hex(text):
    try:
        int(text, 16)
        return True
    except:
        return False
