class StaticCodeAnalyzer:

    # Dictionary with code-message classified by type of issue:
    # "S" -> Stylistic
    code_message = {"S": {1: "Too long"}}

    def __init__(self, file_path):
        self.file_content = self.read_file_lines(file_path)

    @staticmethod
    def read_file_lines(file_path):
        with open(file_path, 'r') as file:
            return file.read().splitlines()

    def print_line_issue(self, line_num, issue_type, issue_num):
        code = issue_type + str(issue_num).zfill(3)
        msg = self.code_message[issue_type][issue_num]
        print(f'Line {line_num}: {code} {msg}')

    def long_lines(self) -> 'prints lines exceeding 79 characters':
        for line_num, content in enumerate(self.file_content):
            if len(content) > 79:
                self.print_line_issue(line_num + 1, "S", 1)

    def run(self):
        self.long_lines()


file_path = input()
code_analyzer = StaticCodeAnalyzer(file_path)
code_analyzer.run()
