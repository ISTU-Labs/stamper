import bcrypt


def get_hashed_password(plain_text_password):
    # Хэширует пароль в фазе его задания
    # Используется модуль bcrypt, соль записывается в сам хэш
    plain_text_password = as_bytes(plain_text_password)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Проверка пароля. В модуле bcrypt соль записана в самом хеше
    plain_text_password = as_bytes(plain_text_password)
    return bcrypt.checkpw(plain_text_password, hashed_password)


def as_bytes(s):
    if type(s) == str:
        return s.encode('utf-8')
    return s
