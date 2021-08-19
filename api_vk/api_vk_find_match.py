import requests


class VkMatch:
    # экземпляр класса на вход будет принимать словарь с данными пользователя, для которого ищем пару
    def __init__(self, user_features, token):
        self.user_features = user_features
        self.token = token

    # метод поиска людей по заданным критериям
    def find_a_people(self):
        url = 'https://api.vk.com/method/users.search'
        # для противоположного пола напишем функцию:
        opposite_sex = lambda x: 1 if x == 2 else 2
        params = {
            'count': 1000,
            'city': self.user_features['city']['id'],
            'sex': opposite_sex(self.user_features['sex']),
            # 1, 5, 6 это статусы, которые говорят о том, что пользователь не занят
            'status': 1 or 5 or 6,
            'age_from': (int(self.user_features['bday']) - 1),
            'age_to': (int(self.user_features['bday']) + 1),
            'access_token': self.token,
            'fields': 'photo_max_orig',
            'v': '5.131',
            'has_photo': 1
        }
        response = requests.get(url, params=params).json()['response']['items']
        # вернем список id пользователей, которые подходят под условия
        id_list = [response[i]['id'] for i in range(len(response))]
        return id_list

    # метод для получения id топ-3 популярных фото пользователя
    def get_photos(self, link):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': link,
            'access_token': self.token,
            'v': '5.130',
            'album_id': 'profile',
            'photo_sizes': '1',
            'extended': '1'
        }
        try:
            list_of_photo = requests.get(url, params=params).json()['response']['items']
            # вычислим сумму комментариев и лайков для каждой фото
            likes_and_comments_list = [(photo['likes']['count'] + photo['comments']['count'])
                                       for photo in list_of_photo]
            # найдем топ-3 популярных фото
            most_popular_photos_indexes = []
            for i in range(3):
                max_index = likes_and_comments_list.index(max(likes_and_comments_list))
                most_popular_photos_indexes.append(max_index)
                likes_and_comments_list[max_index] = 0
            # возвращаем photo_id топ-3 популярных фото
            return list(set(list_of_photo[photo_index]['id'] for photo_index in most_popular_photos_indexes))
        except KeyError:
            return "Приватный профиль"

    # генератор для возврата id владельца фото и id самих топ-3 фото
    def gen(self):
        for photo in self.find_a_people():
            if self.get_photos(photo) != "Приватный профиль":
                yield photo,self.get_photos(photo)
