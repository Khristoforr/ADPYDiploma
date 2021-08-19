import requests


# поиск id города по названию
def find_a_city(token, city):
    url = 'https://api.vk.com/method/database.getCities'
    params = {
        'country_id': 1,
        'need_all': 1,
        'count': 1000,
        'access_token': token,
        'v': '5.130',
        'q': city
    }
    try:
        response = requests.get(url, params=params).json()['response']
        if response['count'] != 1:
            return "Ошибка"
        else:
            return response['items'][0]['id']
    except:
        return "Ошибка"
