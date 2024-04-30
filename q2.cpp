#include <iostream>
#include <iterator>
#include <regex>
#include <string>
#include <thread>
#include <vector>
#include <mutex>

using namespace std;

mutex mtx;

string genStrB(size_t len)
{
    string s;
    for (size_t i = len; i > 0; i /= 3)
    {
        s += 'a' + i % 3;
    }
    return s;
}

string genStrA(size_t len)
{
    string s;
    for (size_t i = len; i > 0; i /= 2)
    {
        s += 'a' + i % 2;
    }
    return s;
}

bool shouldMatchB(string input)
{
    size_t ab = 0;
    size_t ac = 0;
    size_t ba = 0;
    for (size_t i = 0; i < input.size() - 1; i++)
    {
        if (input[i] == 'a' && input[i + 1] == 'b')
            ab++;
        if (input[i] == 'a' && input[i + 1] == 'c')
            ac++;
        if (input[i] == 'b' && input[i + 1] == 'a')
            ba++;
    }
    return ab + ac == ba;
}

bool shouldMatchA(string input)
{
    size_t ab = 0;
    size_t ac = 0;
    size_t ba = 0;
    for (size_t i = 0; i < input.size() - 1; i++)
    {
        if (input[i] == 'a' && input[i + 1] == 'b')
            ab++;
        if (input[i] == 'b' && input[i + 1] == 'a')
            ba++;
    }
    return ab == ba;
}

void testThredB(size_t num, string regex, size_t offset, bool showProgress)
{
    std::regex self_regex(regex, std::regex_constants::ECMAScript | std::regex_constants::icase);
    for (size_t i = offset; i < num + offset; i++)
    {
        string s = genStrB(i);
        bool act = std::regex_match(s, self_regex);
        bool exp = shouldMatchB(s);
        if (act != exp)
        {
            lock_guard<mutex> lock(mtx);
            cout << "Error for:  \"" << s << "\"\t"
                 << "actual:" << (act ? "Accepted" : "Rejected") << "\texpected: " << (exp ? "Accepted" : "Rejected") << endl;
        }
        if (showProgress && i % 10000 == 0)
            cout << i << " like " << s << endl;
    }
}

void testThredA(size_t num, string regex, size_t offset, bool showProgress)
{
    std::regex self_regex(regex, std::regex_constants::ECMAScript | std::regex_constants::icase);
    for (size_t i = offset; i < num + offset; i++)
    {
        string s = genStrA(i);
        bool act = std::regex_match(s, self_regex);
        bool exp = shouldMatchA(s);
        if (act != exp)
        {
            lock_guard<mutex> lock(mtx);
            cout << "Error for:  \"" << s << "\"\t"
                 << "actual:" << (act ? "Accepted" : "Rejected") << "\texpected: " << (exp ? "Accepted" : "Rejected") << endl;
        }

        if (showProgress && i % 10000 == 0)
            cout << i << " like " << s << endl;
    }
}

void test(size_t num, string regex, size_t threads, char question, bool showProgress)
{
    size_t pieceSize = num / threads;
    // cout << "Piece size: " << pieceSize << endl;
    auto testThred = (question == 'a' || question == 'A') ? testThredA : testThredB;
    std::vector<std::thread> threadPool;
    for (size_t i = 0; i < threads; i++)
    {
        threadPool.emplace_back(thread(testThred, pieceSize, regex, i * pieceSize + 1, showProgress));
    }
    for (auto &th : threadPool)
        th.join();
}
int main(int argc, char **argv)
{
    string reg;
    size_t num;
    size_t threads;
    char question;
    bool showProgress = false;
    if (argc > 1 && string(argv[1]) == "-p")
    {
        showProgress = true;
    }

    cout << "Enter questions number (a/b): ";
    cin >> question;
    if (question != 'a' && question != 'b' && question != 'A' && question != 'B')
    {
        cout << "Invalid question number" << endl;
        return 1;
    }

    cout << "Enter regex: ";
    cin >> reg;
    cout << "Enter number of strings to test (in thousands, 1 = 1k): ";
    cin >> num;
    num <<= 10;
    cout << "Enter number of threads: ";
    cin >> threads;

    test(num, "^(" + reg + ")$", threads, question, showProgress);
    return 0;
}