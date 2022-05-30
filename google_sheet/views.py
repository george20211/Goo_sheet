import logging
import redis
from .forms import Sheet_Form
from .models import Google_sheet
from .tasks import google_service
from .centrobank import RateCentralbank
from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
from google_service.celery import app


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)
logger = logging.getLogger(__name__)

class ServicePage:

    # Пагинация результатов вывода таблицы для главной страницы
    def paginators(request, pages, count_pages):
        paginator = Paginator(pages, count_pages)
        paged = request.GET.get('page')
        return paginator.get_page(paged)

    # Функция старта программы
    def start_check_sheet(request):
        google_sheet_list = Google_sheet.objects.all()
        form = Sheet_Form()
        page = ServicePage.paginators(request, google_sheet_list, 15)
        value_id = redis_instance.get('processed')
        if value_id is not None:
            context = {
                'page': page,
                'form': form,
                'process': True
                }
        else:
            context = {
                'page': page,
                'form': form
            }
        logger.info('Открылась главная страница')
        rate = RateCentralbank.rate_dollar()
        start=True
        if request.method == 'POST':
            form = Sheet_Form(request.POST)
            # Валидируем данные из формы, если все ок - запускаемся
            if form.is_valid():
                #start_while.delay(form, start, rate)
                update_rate = form.cleaned_data.get("update_rate")
                name_list = form.cleaned_data.get("name_list")
                first_table = form.cleaned_data.get("first_table")
                last_table = form.cleaned_data.get("last_table")
                update_sheet = form.cleaned_data.get("update_sheet")
                user_id = form.cleaned_data.get("telegram_msg")
                telegram_id = form.cleaned_data.get("telegram_id")
                logger.info('Проверка пользовательских данных')
                if value_id is not None:
                    app.control.revoke(str(value_id.decode('utf-8')), terminate=True)
                    redis_instance.delete('processed')
                process = google_service.delay(
                            start, rate, update_rate, name_list,
                            first_table, last_table, update_sheet,
                            user_id, telegram_id
                            )
                redis_instance.set('processed', process.id)
                context = {
                    'page': page,
                    'form': form,
                    'process': True
                }
                return render(request, "google_sheet/panel.html", context)
            else:
                logger.info('данные пользователя не прошли проверку')
                return render(request, "google_sheet/panel.html", context)
        return render(request, "google_sheet/panel.html", context)
