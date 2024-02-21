import re

BEST_LEN = 15

def any_match(string, match_list):
    result = []
    for match in match_list:
        if string.find(match) != -1:
            result.append(match)
    return result


def any_match_bool(string, match_list):
    for match in match_list:
        if string.find(match) != -1:
            return True
    return False


def extract_digit(string):
    result = ""
    for ch in string:
        if ch.isdigit():
            result += ch
    return result


def transfer_hump_to_database_name(string):
    # schoolAddress -> school_address
    result = ""
    for ch in string:
        if ch.isupper():
            result = result + '_' + ch.lower()
        else:
            result += ch
    return result


def find_all(string, substring):
    positions = []
    start = string.find(substring)

    while start != -1:
        positions.append(start)

        # 更新起始位置为当前子串后面的位置
        start += len(substring)
        next_pos = string[start:].find(substring)
        if next_pos == -1:
            break
        start = next_pos + start

    return positions

#去掉所有的空格、回车等特殊符号
def remove_special_symbols(string):
    return string.replace("\n", "").replace("\r", "").replace("\b", "").replace("\t", "").replace(" ", "")


def has_chinese(sentence):
    for ch in sentence:
        if is_chinese(ch):
            return True
    return False


# ---------------------------功能:判断字符是不是汉字-------------------------------
def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False


def handle_short_sentence(segment_list):
    temp_split_pos_list = []
    i = 0
    while i < len(segment_list) - 1:
        cur_seg_begin, cur_seg_end = segment_list[i]
        next_seg_begin, next_seg_end = segment_list[i+1]
        if cur_seg_end - cur_seg_begin < BEST_LEN and next_seg_end - next_seg_begin < BEST_LEN:
            temp_split_pos_list.append((cur_seg_begin, next_seg_end))
            i += 2
        else:
            temp_split_pos_list.append((cur_seg_begin, cur_seg_end))
            i += 1
    if i < len(segment_list):
        temp_split_pos_list.append(segment_list[i])
    return temp_split_pos_list


def split_text(text):
    if text == '-':
        return []
    text = remove_special_symbols(text)
    split_pos_list = []
    begin = 0
    for pos in find_all(text, "。"):
        split_pos_list.append((begin, pos))
        begin = pos+1
    split_pos_list.append((begin, len(text)))

    #TODO 长句处理
    #短句处理
    split_pos_list = handle_short_sentence(split_pos_list)
    split_text_list = []
    for begin, end in split_pos_list:
        if begin >= end:
            continue
        split_text_list.append(text[begin: end])
    return split_text_list
    # return re.split("。", text)