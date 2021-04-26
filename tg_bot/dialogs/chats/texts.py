from aiogram import types


def mention(message: types.Message):
    return message.from_user.get_mention(message.new_chat_members[0].mention if message.new_chat_members else message.from_user.mention)

url_in_last_posts = lambda m, c: f"{mention(m)}, Такая ссылка уже была, дождитесь {c.posts_count} постов!"

region = "Привет! Конкурсы и гранты какого региона Вам нужны?\nВведите название региона. Например, Республика Татарстан."
region__try_again = "Извините, такого региона нет в нашей базе. Отправьте регион снова, а лучше выберите из выпадающего списка."
form = "От лица кого планируете подавать заявки. Выберите:"
form__try_again = "Извините, такого лица нет в нашей базе. Отправьте ей снова, а лучше выберите из кнопок."
type_category = "Направление поддержки в конкурсе по которому хотите получать анонсы"
type_category__try_again = "Извините, такой категории нет в нашей базе. Отправьте ей снова, а лучше выберите из кнопок."

