import re
import sys
import os


class StaticCodeAnalyzer:

    # Dictionary with code-message classified by type of issue:
    # "S" -> Stylistic
    code_message = {"S": {1: "Too long",
                          2: "Indentation is not a multiple of four",
                          3: "Unnecessary semicolon after a statement",
                          4: "Less than two spaces before inline comments",
                          5: "TODO found",
                          6: "More than two blank lines preceding a code line"}}

    def __init__(self, path: str):
        self.main_path = path
        self.file_path = ""
        self.file_content = []
        self.line_num = 0
        self.line_content = ""
        self.blank_lines = 0

    @staticmethod
    def read_file_lines(file_path) -> 'returns file contents as a list of its lines':
        with open(file_path, 'r') as file:
            return file.read().splitlines()

    def print_line_issue(self, issue_type: str, issue_num: int) -> \
            'prints issue with format "Path: Line X: Code Message"':
        code = issue_type + str(issue_num).zfill(3)
        msg = self.code_message[issue_type][issue_num]
        print(f'{self.file_path}: Line {self.line_num + 1}: {code} {msg}')

    def check_style(self):
        # Iterates over all style codes in self.code_message dictionary
        for issue_num in self.code_message["S"]:
            # Get method name dynamically
            s_x = getattr(self, "s_" + str(issue_num))
            if s_x():
                self.print_line_issue("S", issue_num)

    def s_1(self) -> 'returns True if line exceeds 79 characters':
        return len(self.line_content) > 79

    def s_2(self) -> 'returns True if line indentation is not multiple of four':
        # Check that first character is not a whitespace
        return (len(self.line_content) - len(self.line_content.lstrip())) % 4 != 0 and self.line_content[0] == " "

    def s_3(self) -> 'returns True if semicolon after a statement':
        pattern = r";\s*$"
        return re.search(pattern, self.split_statement_comment(self.line_content)[0])

    def s_4(self) -> 'returns True if less than two spaces before inline comment':
        line_split = self.split_statement_comment(self.line_content)
        return len(line_split) > 1 and line_split[0] not in "'''#" \
            and (len(line_split[0]) - len(line_split[0].rstrip())) < 2

    def s_5(self) -> 'returns True if TODO found in comments':
        line_split = self.split_statement_comment(self.line_content)
        pattern = "TODO"
        if len(line_split) > 1:
            line_comment = line_split[1]
        elif self.is_code(line_split[0]):
            return False
        else:
            line_comment = line_split[0]
        return re.search(pattern, line_comment, re.IGNORECASE)

    def s_6(self) -> 'returns True if more than two blank lines before a code line':
        result = self.is_code(self.line_content) and self.blank_lines > 2
        self.blank_lines = self.blank_lines + 1 if not self.line_content else 0
        return result

    @staticmethod
    def is_code(string: str) -> "returns True if it's a code line":
        pattern = "('''|#)"
        return not re.match(pattern, string) and bool(string)

    @staticmethod
    def split_statement_comment(string: str) -> 'returns string split in code and comment':
        return string.split('#')

    def run(self):
        # Check if it's file or directory
        if self.main_path.endswith(".py"):
            self.file_path = self.main_path
            self.file_content = self.read_file_lines(self.file_path)
            for self.line_num, self.line_content in enumerate(self.file_content):
                self.check_style()
        else:
            # List all files in the directory using scandir()
            with os.scandir(self.main_path) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith(".py") and entry.name != "tests.py":
                        self.file_path = self.main_path + '\\' + entry.name
                        self.file_content = self.read_file_lines(self.file_path)
                        for self.line_num, self.line_content in enumerate(self.file_content):
                            self.check_style()

path = sys.argv[1]
code_analyzer = StaticCodeAnalyzer(path)
code_analyzer.run()
