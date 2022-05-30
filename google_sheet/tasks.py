import os
import datetime as dt
import time
import logging
from .models import Google_sheet
from .centrobank import RateCentralbank
from .telegram_send import SenderMessages
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_service.settings import BASE_DIR
from google_service.celery import app

logger = logging.getLogger(__name__)

@app.task(name='Google_sheet')
def google_service(start, rate, update_rate, name_list,
                            first_table, last_table, update_sheet,
                            telegram_msg, user_id):
        # Уровень доступа, который получит это приложение (Только чтение)
        ACCESS_LEVEL_READ = [os.getenv('ACCESS_LEVEL_READ')]
        # ID таблицы Google Sheet (берется из URL адреса таблицы)
        SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
        # Старт таймера для обновления курса доллара каждый час
        timer_for_rate = dt.datetime.now()
        timer_start = time.time()
        first_ms_start = True
        # Запускаем бесконечное сканирование таблиц
        while start:
            timer_in_cycle = time.time()
            # Делаем наш запрос авторизованным
            CREDS = Credentials.from_authorized_user_file(
                        os.path.join(BASE_DIR, 'token.json'),
                        ACCESS_LEVEL_READ
                        )
            # Метод googleapiclient.discovery.build
            # для работы с любым API Google
            SERVICE = build('sheets', 'v4', credentials=CREDS, cache_discovery=False)
            # 'name_list' - Название нужного листа. (строка в строке)
            # 'first_table' Начало считывания (с буквы столбца таблицы)
            # 'last_table' Конец считывания (до буквы столбца таблицы)
            RANGE_NAME = f"'{name_list}'!{first_table}:{last_table}"
            # Сколько секунд прошло с момента обновления курса ЦБ
            second_passed = (dt.datetime.now() - timer_for_rate).seconds
            # Если прошло больше секуд чем 'update_rate', обновляем
            # данные курса и обнуляем переменную timer_for_rate
            if second_passed > update_rate:
                rate = RateCentralbank.rate_dollar()
                timer_for_rate = dt.datetime.now()
            # Получаем кортеж данных: 'range', 'majorDimension', 'values'.
            # Где список values значения наших таблиц
            result = SERVICE.spreadsheets().values().get(
                                                spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME,
                                                ).execute()
            # id которые уже есть в базе данных
            all_data = Google_sheet.objects.all()
            id_in_DB = all_data.values('id')
            # Создадим список для хранения существующих id в Google sheet
            sheet_id_list = []
            # Будущий "список" просроченных дат в виде строки
            message_data = ''
            # Если введут не существующую тублицу/ячейку
            try:
                # Перебираем строки таблиц в списке 'values'
                for row in result['values']:
                    """Если таблица в Google sheet заполняется данными в момент считывания,
                    или одна из таблиц содержит не верные данные,
                    блок try/except позволит пропустить не завершенную
                    или с ошибкой строку в таблице
                    и продолжить выполнение сценария, если значение исправят на
                    корректное - строка будет добавлена в БД со
                    следующей итерацией цикла"""
                    try:
                        # Создаем переменную с данными в рублях
                        # по курсу на сегодня
                        # ограничиваем цифры после запятой до 4
                        row_4 = round(float(row[2]) * float(rate), 4)
                        # Заполняем кортеж данными
                        updated_values = {
                            'id': int(row[0]),
                            'order': int(row[1]),
                            'price_usd': float(row[2]),
                            'delivery_time': dt.datetime.strptime(row[3],
                                                                  '%d.%m.%Y'),
                            'price_rub': row_4,
                        }
                        # Если модели с заданным id нет - создаем из кортежа,
                        # если уже есть - обновляем данные из кортежа
                        Google_sheet.objects.update_or_create(
                            id=int(row[0]),
                            defaults=updated_values
                            )
                        # Добавляем id в список
                        sheet_id_list.append(int(row[0]))
                        if updated_values['delivery_time'] < timer_for_rate:
                            # Прибавляем новую информацию в
                            # строку для отправки в телеграм
                            message_data += f'[id: {row[0]}]  |заказ: {row[1]}, просрочен: {row[3]}\n'
                    # Обработка ошибки если таблица в
                    # процессе заполнения юзером
                    except IndexError:
                        msg = f"В строке таблицы заполнены не все поля - {row}"
                        logger.warning(msg)
                        continue
                    # Обработка ошибки если в
                    # строке таблицы не верный формат данных
                    except ValueError:
                        msg = ("В одно из полей таблицы ",
                               "поступил не верный формат")
                        logger.warning(msg)
                        continue
            except KeyError:
                msg = "Не найден номер ячейки таблицы"
                logger.warning(msg)
                continue
            # Если в базе данных остались строки с id которых
            # нет в Google sheet - удаляем из базы
            for obj in id_in_DB:
                # Если id в базе данных существует в списке Google sheet
                if int(obj['id']) in sheet_id_list:
                    continue
                # Если id в базе есть, но нет в
                # Google sheet - удалить лишний объект
                else:
                    Google_sheet.objects.filter(id=int(obj['id'])).delete()
            # Тут решаем пора ли отправлять сообщение в телеграм
            # Зависит от настроек пользователя на панели
            difference = int(timer_in_cycle)-int(timer_start)
            if telegram_msg < difference or first_ms_start == True:
                timer_start = time.time()
                first_ms_start = False
                timer_in_cycle = time.time()
                SenderMessages.sended_message(message_data, user_id)
            # Время проверки обновлений в Google sheets (секунды)
            time.sleep(update_sheet)