import requests  
import datetime
 
class BotHandler:
 
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.users = []
 
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
 
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
 
    def get_last_update(self):
        get_result = self.get_updates()
        try:
            if len(get_result) > 0:
                last_update = get_result[-1]
            else:
            
                last_update = get_result[len(get_result)]
            return last_update
        except:
            return ""

    def add_user(self, user_id):
        self.users.append(user_id)

    def get_users(self):
        return self.users
        

class CalculatingResult:
    
    def __init__(self, number):
        self.number = number

    def len_number(self):
        return len(self.number)

    def get_count_number(self, try_number):
        count = 0
        if len(try_number) == len(self.number):
            for i in range(len(self.number)):
                for j in range(len(try_number)):
                    if self.number[i] == try_number[j]:
                        count = count + 1
        return count

    def get_right_number(self, try_number):
        count = 0
        if len(try_number) == len(self.number):
            for i in range(len(self.number)):
                if self.number[i] == try_number[i]:
                    count = count + 1
        return count

    def is_len(self, try_number):
        if len(try_number) == len(self.number):
            return True
        return False

    def repetition_of_numbers(self, number):
        for i in range(len(number)):
            for j in range(i + 1, len(number)):
                if number[i] == number[j]:
                    return False
        return True

greet_bot = BotHandler('683263627:AAGDtQbFHCAXYA2_YVoIzd8064vaAgx3hRc')  

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():  
    new_offset = None
    is_win = True
    count = 0
    game_bot = CalculatingResult("12345")

    win_id = ''
    guessing_id = ''

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if(len(last_update) > 0):
            last_update_id = last_update['update_id']
            new_offset = last_update_id + 1
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if represents_int(last_chat_text):

                    
                greet_bot.add_user(last_update_id)

                if last_chat_id != guessing_id:
                    if bool(is_win):
                        if game_bot.get_right_number(last_chat_text) == len(last_chat_text):
                            win_id = last_chat_id
                            greet_bot.send_message(last_chat_id, "Ты победил введи число")
                            
                            for i in range(len(greet_bot.get_users())):
                                greet_bot.send_message(greet_bot.get_users()[i], last_chat_name + " -> Попыток - " + str(count + 1))
                            is_win = False
                            count = 0
                        else:
                            if game_bot.repetition_of_numbers(last_chat_text):
                                if game_bot.is_len(last_chat_text):
                                    count = count + 1
                                    greet_bot.send_message(last_chat_id, str(count) + " " + last_chat_text + " " + str(game_bot.get_count_number(last_chat_text)) + " " + str(game_bot.get_right_number(last_chat_text)))
                                else:
                                    greet_bot.send_message(last_chat_id, "Введите правильно длину! Длина = " + str(game_bot.len_number()))
                            else:
                                greet_bot.send_message(last_chat_id, "Числа повторяются!")
                            
                    else:
                        if game_bot.repetition_of_numbers(last_chat_text):
                            game_bot = CalculatingResult(last_chat_text)
                            guessing_id = last_chat_id
                            is_win = True
                        else:
                            greet_bot.send_message(last_chat_id, "Числа повторяются!")
                else:
                    greet_bot.send_message(last_chat_id, "Ты загадал число")
            else:
                greet_bot.send_message(last_chat_id, "Ты ввел не только цыфры")
         
            
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
