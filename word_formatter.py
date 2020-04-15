import string
import re

ascii_chars = set(string.printable)


def contain_number(st):
    for s in st.split(' '):
        if s.isnumeric():
            return True
    return False


def contain_letter(st):
    for c in st:
        if ord('a') <= ord(c) <= ord('z'):
            return True
        if ord('A') <= ord(c) <= ord('Z'):
            return True
    return False


def get_number(st):
    for s in st.split(' '):
        if s.isnumeric():
            return s
    raise Exception("string to int error on: " + st)


def remove_non_ascii(st):
    global ascii_chars
    result = ''
    ok = True
    for character in st:
        if character == ' ' or character == '\n':
            if ok:
                result = result + ' '
        elif character in ascii_chars:
            if not ok:
                result = result + '$'
            result = result + character
            ok = True
        else:
            ok = False
    return result


def line_to_tuple(st):
    line_number = get_number(st)
    st = remove_non_ascii(st)
    first_arr = re.split('[\d$]', st)
    arr = [line_number]
    for x in first_arr:
        if contain_letter(x.strip()):
            arr.append(x.strip().replace(';', ','))
    assert len(arr) == 3
    if len(arr[1].split(',')) > 1 and not len(arr[2].split(',')) > 1:
        arr[1], arr[2] = arr[2], arr[1]
    return ';'.join(arr)


with open('Files/words.txt', newline='') as file:
    last_lines = ''
    for line in file:
        correct_line = line.replace('\n', ' ')
        if not contain_number(correct_line):
            last_lines = last_lines + correct_line
        else:
            if len(last_lines.strip()) > 0:
                print(line_to_tuple(last_lines))
            last_lines = correct_line
    if len(last_lines) > 0:
        print(line_to_tuple(last_lines))
