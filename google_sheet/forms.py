from django import forms
from .validators import update_rate, update_sheet, telegram_msg

#Формы ввода для html страницы
class Sheet_Form(forms.Form):
    update_rate = forms.IntegerField(validators=[update_rate],
                                     initial=300,
                                     label='Время обновления курса валюты от '
                                     'ЦБ в секундах(min 60)')
    name_list = forms.CharField(label='Название нужного листа'
                                'отображается в низу страницы Google sheets',
                                initial='Лист1',
                                max_length=50)
    first_table = forms.CharField(max_length=7,
                                  initial='A2',
                                  label='Начало считывания со столбца "A".'
                                  'Цифра-номер строки с которой начать. '
                                  'Если указать просто цифру, будет начало '
                                  'считывания с номера id первого столбца')
    last_table = forms.CharField(max_length=7,
                                 initial='D',
                                 label='Конец считывания - столбец "D" '
                                 'Если цифра не указана - считывать до '
                                 'последней существующей строки. '
                                 'Если указать просто цифру, '
                                 'конец считывания до номера id '
                                 'всех существующих столбцов.')
    update_sheet = forms.IntegerField(validators=[update_sheet],
                                      initial=5,
                                      label='Каждые X секунд обновляет '
                                      'данные из Google sheets(min 3).')
    telegram_msg = forms.IntegerField(validators=[telegram_msg],
                                      initial=3600,
                                      label='При старте бота и каждые Х секунд'
                                      ' будет приходить список просроченных'
                                      ' поставок в чат-бота '
                                      '(min каждые 10 минут == 600 сек).')
    telegram_id = forms.CharField(initial='None',
                                  label='ВАШ id ЧАТА TELEGRAM! если нужны уведомления')
