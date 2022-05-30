from django.core.exceptions import ValidationError


# Проверяем входящее значение update_rate
# (обновление курса с ЦБ) из html страницы
def update_rate(update_rate):
    if update_rate is not int() and update_rate < 60:
        raise ValidationError(
            ('Недопустимое значение (%(update_rate)s) в первом поле формы. '
             'Минимально-возможное время получения данных от ЦБ - 21 секунда. '
             'РЕКОМЕНДУЕМОЕ 300 секунд'), params={'update_rate': update_rate},
            )


# Проверяем входящее значение update_sheet
# (обновление таблиц в БД) из html страницы
def update_sheet(update_sheet):
    if update_sheet is not int() and update_sheet < 3:
        raise ValidationError(
            ('Недопустимое значение (%(update_sheet)s)',
             'в предпоследнем поле формы. ',
             'Минимально-возможное время получения данных',
             'от Google sheets - 3 секунды. ',
             'Минимально-рекомендуемое 5 секунд. '),
             params={'update_sheet': update_sheet},
            )

# Как часто будут приходить списки в телеграм
def telegram_msg(telegram_msg):
    if telegram_msg is not int() and telegram_msg < 10:
        raise ValidationError(
            ('Недопустимое значение (%(telegram_msg)s) в последнем поле.'),
            params={'telegram_msg': telegram_msg},
        )
