import re
import random

regex = r'^(REPLACE_ME_WITH_YOUR_REGEX)$'

def count_AB(string):
    count = 0
    for i in range(len(string) - 1):
        if string[i] == 'a' and string[i + 1] == 'b':
            count += 1
    return count


def count_AC(string):
    count = 0
    for i in range(len(string) - 1):
        if string[i] == 'a' and string[i + 1] == 'c':
            count += 1
    return count


def count_BA(string):
    count = 0
    for i in range(len(string) - 1):
        if string[i] == 'b' and string[i + 1] == 'a':
            count += 1
    return count


def valid(string):
    for char in string:
        if char not in ['a', 'b', 'c']:
            return False
    return True


counter = 0


def run(string):
    global regex, counter
    string = string.strip()
    ref = (count_AB(string) + count_AC(string)
           == count_BA(string)) and valid(string)
    tested = bool(re.match(regex, string))
    if tested != ref:
        print(f"Failed: {string} => [(exp:{ref} !== act:{tested}) => (ab {count_AB(string)} + ac {count_AC(string)} = ba {count_BA(string)})] => count: {counter}")
        counter += 1
        return


def generate_string(n):
    string = ""
    for i in range(n):
        string += chr(97 + random.randint(0, 2))
    return string


def generate_string_sequential(n,length):
    string = ""
    while n > 0:
        string = chr(97 + n % 3) + string
        n = n // 3
    while len(string) < length:
        string = "a" + string
    return string


def test_sequential(num):
    for i in range(1, num + 1):
        size =  3 ** (i)
        print("Length of ", i, "has",size, "strings")
        for j in range(0, size):
            run(generate_string_sequential(j, i))

def test(num):
    for _ in range(num):
        run(generate_string(100))


test_sequential(5)
