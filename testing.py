import unittest
from nfa import Compiler
from regex import Regex


class TestRegex(unittest.TestCase):
    def base(self, fname):
        with open(fname) as f:
            self.text = f.readlines()

        for line in self.text:
            llist = line.split()
            f_str = None
            if len(llist) == 2:
                [pattern, t_str] = llist
            elif len(llist) == 3:
                [pattern, t_str, f_str] = llist
            re = Regex(pattern)
            nfa = Compiler(re.postfix)
            print(f"TESTING {pattern}...")
            self.assertEqual(nfa.automata.match(t_str), True)
            if f_str:
                self.assertEqual(nfa.automata.match(f_str), False)
            print(line, "pass")

    def test_basic(self):
        self.base('testing/test_suite.dat')


if __name__ == '__main__':
    unittest.main()
