import re
import random

regex = r'^(REPLACE_THIS_TEXT_WITH_YOUR_REGULAR_EXPRESSION)$'


def countAB(string):
    count = 0
    for i in range(len(string) - 1):
        if string[i] == 'a' and string[i + 1] == 'b':
            count += 1
    return count


def countBA(string):
    count = 0
    for i in range(len(string) - 1):
        if string[i] == 'b' and string[i + 1] == 'a':
            count += 1
    return count


def valid(string):
    for char in string:
        if char != 'a' and char != 'b':
            return False
    return True


counter = 0


def run(string):
    global regex, counter
    string = string.strip()
    ref = (countAB(string) == countBA(string)) and valid(string)
    tested = re.match(regex, string)
    if tested is not None and tested.group() == string:
        tested = True
    else:
        tested = False
    if tested != ref:
        print(f"Failed: {string} => [(exp:{ref} !== act:{tested}) => (ab {
              countAB(string)} = ba {countBA(string)})] => count: {counter}")
        counter += 1
        return


def generateString(n):
    string = ""
    for _ in range(n):
        string += chr(97 + random.randint(0, 1))
    return string


def generateStringSequential(n):
    string = ""
    while n > 0:
        string += chr(97 + n % 2)
        n = n // 2
    return string


def testSequential(num):
    for i in range(1, num):
        run(generateStringSequential(i))


def test(num):
    for _ in range(num):
        run(generateString(100))


testSequential(100000)
