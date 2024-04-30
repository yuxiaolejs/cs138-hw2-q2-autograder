import re
import random

regex = r'^(REPLACE_THIS_TEXT_WITH_YOUR_REGULAR_EXPRESSION)$'

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
        print(f"Failed: {string} => [(exp:{ref} !== act:{tested}) => (ab {count_AB(
            string)} + ac {count_AC(string)} = ba {count_BA(string)})] => count: {counter}")
        counter += 1
        return


def generate_string(n):
    string = ""
    for i in range(n):
        string += chr(97 + random.randint(0, 2))
    return string


def generate_string_sequential(n):
    string = ""
    while n > 0:
        string += chr(97 + n % 3)
        n = n // 3
    return string


def test_sequential(num):
    for i in range(1, num):
        if (i % 10000 == 0):
            print(f"Testing {i}th string")
        run(generate_string_sequential(i))


def test(num):
    for _ in range(num):
        run(generate_string(100))


test_sequential(100000)
