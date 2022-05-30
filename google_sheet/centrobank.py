import logging
import requests
import time
from bs4 import BeautifulSoup
from urllib.error import HTTPError

logger = logging.getLogger(__name__)

class RateCentralbank:
    # Считаем курс доллара на сегодня
    @classmethod
    def rate_dollar(cls) -> float:
        # Пока не получим актуальный курс - не уйдем
        while True:
            try:
                all_rate_text = requests.get('https://www.cbr.ru/scripts/XML_daily.asp'
                                        ).text
                rate_as_str = BeautifulSoup(all_rate_text,
                                    features='xml'
                                    ).Value.string
                dollar_rate = float(rate_as_str.replace(',', '.'))
                return dollar_rate
            except AttributeError:
                msg = ('Не получены данные по курсу!',
                        'Повторная попытка через минуту!')
                logger.warning(msg)
                time.sleep(60)
            except HTTPError:
                msg = 'API ЦБ отказался принять запрос или URL изменился!'\
                        'Повторная попытка через минуту!'
                logger.warning(msg)
                time.sleep(60)
