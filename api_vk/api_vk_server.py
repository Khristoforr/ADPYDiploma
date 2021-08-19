import requests

# Получим токен сообщества из файла
with open('C:\\Users\\tiger\OneDrive\Рабочий стол\Учеба в Нетологии\Projects\AdvancedPythonDiploma\\api_vk\pass.txt',
          'r', encoding='utf-8') as f:
    VK_GROUP_TOKEN = f.readline()


class VkServer:
    # метод, отвечающий за получение сообщения от пользователя в чате,
    def get_message_from_user(self):
        url = 'https://api.vk.com/method/groups.getLongPollServer'
        params = {
            'group_id': 47378589,
            'access_token': VK_GROUP_TOKEN,
            'v': '5.131',
        }
        # получение данных сессии
        session_data = requests.get(url, params=params).json()['response']
        response = requests.get(
            '{server}?act=a_check&key={key}&ts={ts}&wait=25'
                .format(server=session_data['server'], key=session_data['key'], ts=session_data['ts'])).json()
        text = response['updates'][0]['object']['message']['text']
        user_id = response['updates'][0]['object']['message']['from_id']
        # функция возвращает список из текста, который написал пользователь, и id пользователя
        return [text, user_id]

    # метод, отвечающий за ответ пользователю в чате
    def make_an_answer(self, message, user_id):
        url = 'https://api.vk.com/method/messages.send'
        params = {'groud_id': 47378589,
                  'peer_id': user_id,
                  'access_token': VK_GROUP_TOKEN,
                  'message': message,
                  'v': '5.131',
                  'random_id': 0}
        response = requests.post(url=url, params=params).json()
        return response

    # метод для отправки фото пользователю
    def send_photo_to_user(self, photo_id_list, user_id, photo_owner):
        url = 'https://api.vk.com/method/messages.send'
        if len(photo_id_list) == 1:
            params = {'groud_id': 47378589,
                      'peer_id': user_id,
                      'access_token': VK_GROUP_TOKEN,
                      'message': 'Возможно вам подходит:',
                      'attachment': f'photo{photo_owner}_{photo_id_list[0]}',
                      'v': '5.131',
                      'random_id': 0}
            return requests.post(url=url, params=params).json()
        elif len(photo_id_list) == 2:
            params = {'groud_id': 47378589,
                      'peer_id': user_id,
                      'access_token': VK_GROUP_TOKEN,
                      'message': 'Возможно вам подходит:',
                      'attachment': f'photo{photo_owner}_{photo_id_list[0]},'
                                    f'photo{photo_owner}_{photo_id_list[1]},',
                      'v': '5.131',
                      'random_id': 0}
            return requests.post(url=url, params=params).json()
        elif len(photo_id_list) == 3:
            params = {'groud_id': 47378589,
                      'peer_id': user_id,
                      'access_token': VK_GROUP_TOKEN,
                      'message': 'Возможно вам подходит:',
                      'attachment': f'photo{photo_owner}_{photo_id_list[0]},'
                                    f'photo{photo_owner}_{photo_id_list[1]},'
                                    f'photo{photo_owner}_{photo_id_list[2]}',
                      'v': '5.131',
                      'random_id': 0}
            return requests.post(url=url, params=params).json()
