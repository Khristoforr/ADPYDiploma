import requests


class VkUser:
    def __init__(self, token):
        self.token = token

    # метод для проверки корректности токена, который вводит пользователь
    def check_token(self):
        params = {
            'user_id': '1',
            'access_token': self.token,
            'v': '5.131',
        }
        response = requests.get('https://api.vk.com/method/users.get', params=params)
        try:
            if response.json()['response'][0]['first_name'] == "Павел":
                print('Токен прошел проверку и принят для дальнейшего использования!')
                return self.token
        except KeyError:
            print("Ошибка! C токеном что-то не так, попробуйте еще раз")

    # метод для получения первичной информации о пользователе
    def get_user_info(self, vk_id):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': vk_id,
            'fields': 'bdate, sex, city, relation',
            'access_token': self.check_token(),
            'v': '5.131',
        }
        # получим первичную информацию о пользователе
        try:
            user_info = requests.get(url, params=params).json()['response'][0]

            # далее необходимо извлечь интересующие нас параметры
            user_correct_info = {}
            for i in ({'relation', 'sex', 'city', 'bday'} & set(user_info)):
                user_correct_info[i] = user_info[i]

            # получим данные о том, какая информация о пользователе отсутствует
            user_absent_info = {}
            for i in ({'relation', 'sex', 'city', 'bday'} - set(user_info)):
                user_absent_info[i] = ''
            # возвращаем данные о пользователе
            return [user_correct_info, user_absent_info]
        except:
            return "Ошибка! введенный id пользователя некорректен"
