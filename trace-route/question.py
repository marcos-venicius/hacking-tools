class Question:
    def __init__(self, options: dict[str, str]):
        self.options = options

    def __max_option_length(self):
        m = 0

        for option in self.options:
            if len(option) > m:
                m = len(option)

        return m

    def ask(self, question: str) -> str:
        print('-' * 100, '\n')

        max_option_length = self.__max_option_length()

        for option in self.options:
            print(str(option).strip().ljust(3, ' '), '    ', self.options[option])

        print()

        while True:
            option = input(question).strip()

            if option not in self.options: continue

            return option

