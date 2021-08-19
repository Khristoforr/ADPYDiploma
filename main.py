from api_vk.api_vk_server import VkServer as VS
from api_vk.api_vk_user import VkUser as VU
from check_user_info import check_info
from api_vk.api_vk_find_match import VkMatch as VM
from menu import *
from database import database


def main():
    running = True
    while running:
        # получим первое сообщение от пользователя
        user_message = VS().get_message_from_user()
        user_id = user_message[1]
        user_text = user_message[0]

        # проверка, что пользователь вводит именно текст
        while user_text == "":
            VS().make_an_answer("Ошибка! Нужно ввести текст", user_id)
            user_text = VS().get_message_from_user()[0]

        # поприветствуем пользователя
        VS().make_an_answer(greetings(), user_id)
        user_message = VS().get_message_from_user()[0]

        # проверка, что пользователь выбирает необходимые параметры
        while user_message != "1" and user_message != "2":
            VS().make_an_answer(check_user_input(), user_id)
            user_message = VS().get_message_from_user()[0]

        # если пользователь выбирает вариант 1
        if user_message == '1':
            VS().make_an_answer("Отлично, продолжим работу. Введите токен для проверки", user_id)
            # получим токен от пользователя
            user_token = VS().get_message_from_user()[0]

            # проверка токена на корректность
            while user_token != VU(user_token).check_token():
                VS().make_an_answer(token_error(), user_id)
                user_token = VS().get_message_from_user()[0]

            VS().make_an_answer(token_accepted(), user_id)
            user_finds_a_pair = VS().get_message_from_user()[0]

            # проверка ID пользователя, которому ищем пару на корректность
            while VU(user_token).get_user_info(user_finds_a_pair) == "Ошибка! введенный id некорректен":
                VS().make_an_answer('Введите корректный id', user_id)
                user_finds_a_pair = VS().get_message_from_user()[0]

            # определяется какая информация о пользователе есть, а какую нужно уточнить
            user_finds_a_pair_info = VU(user_token).get_user_info(user_finds_a_pair)[0]
            user_finds_a_pair_absent_info = VU(user_token).get_user_info(user_finds_a_pair)[1]

            # получим всю информацию о пользователе
            user_all_info = check_info(user_finds_a_pair_info, user_finds_a_pair_absent_info, user_token, user_id)

            # проитерируемся по генератору
            for photo in VM(user_all_info, user_token).gen():
                VS().make_an_answer(message=f'https://vk.com/id{photo[0]}', user_id=user_id)
                VS().send_photo_to_user(photo[1], user_id, photo[0])
                try:
                    database(user_finds_a_pair, f"'https://vk.com/id{photo[0]}")
                except:
                    pass
            VS().make_an_answer('Это все пользователи, удовлетворяющие критериям, хотите повторить поиск? да/нет?',
                                user_id)
            if VS().get_message_from_user()[0].lower() == "нет":
                running = False
            else:
                running = True

        elif user_message == '2':
            VS().make_an_answer("Пока-пока", user_id)
            running = False

        else:
            VS().make_an_answer("Неверная команда, попробуйте еще раз.", user_id)


if __name__ == '__main__':
    main()
