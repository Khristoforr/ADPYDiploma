from api_vk.api_vk_server import VkServer as VS
from api_vk.api_vk_find_city_id import find_a_city


def check_info(user_finds_a_pair_info, user_finds_a_pair_absent_info, user_token, user_id):
    # поочередно запросим у пользователя отсутствующие данные
    for inf in user_finds_a_pair_absent_info.keys():
        if inf == 'city':
            VS().make_an_answer("Введите город пользователя", user_id)
            city = VS().get_message_from_user()[0]
            city_id = find_a_city(user_token, city)
            # проверка на корректность
            while city_id == "Ошибка":
                VS().make_an_answer("Ошибка! Название города введено некорректно. Попробуйте еще раз", user_id)
                city = VS().get_message_from_user()[0]
                city_id = find_a_city(user_token, city)
            user_finds_a_pair_absent_info[inf] = {'id': city_id}
        elif inf == 'bday':
            VS().make_an_answer("Введите возраст пользователя", user_id)
            age = VS().get_message_from_user()[0]
            # проверка на корректность
            while age.isalpha():
                VS().make_an_answer("Некорректно введен возраст, попробуйте еще раз", user_id)
                age = VS().get_message_from_user()[0]
            user_finds_a_pair_absent_info[inf] = age
    user_finds_a_pair_info.update(user_finds_a_pair_absent_info)
    return user_finds_a_pair_info
