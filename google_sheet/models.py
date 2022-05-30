from django.db import models


# Все по ТЗ, никаких записей в базу кроме таблицы Google sheet
class Google_sheet(models.Model):
    # Делаем id заказов уникальными int полями
    # Все поля обязательны для заполнения
    id = models.SmallIntegerField(null=False, db_index=True,
                                  primary_key=True, unique=True,
                                  default='None')
    order = models.IntegerField(null=False, default='None')
    price_usd = models.FloatField(null=False, default='None')
    delivery_time = models.DateField(blank=True, default='None')
    price_rub = models.FloatField(null=False, default='None')

    class Meta:
        # Сортировка по id
        ordering = ('-id',)
        # Человекочитаемые названия
        verbose_name = 'Google sheet'
        verbose_name_plural = 'Google sheets'

    def __str__(self):
        # Возвращаем значения таблиц в виде читаемой строки
        return f'{self.id}'
