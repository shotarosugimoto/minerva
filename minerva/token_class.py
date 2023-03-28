class Token:
    total_token = 0

    def __init__(self, use_token):
        self.use_token = use_token
        Token.total_token += use_token

    @staticmethod
    def create_token_file():
        token_f = open('../docs/token_output.txt', 'w')
        token_f.write('# token usage history\n')
        token_f.close()

    def output_token_information(self, function_name):
        token_f = open('../docs/token_output.txt', 'a')
        token_f.write(f'function_name: {function_name}, use_token: {self.use_token}, '
                      f'total_token: {Token.total_token}\n')
        token_f.close()
