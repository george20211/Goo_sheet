from django.urls import path
from .views import ServicePage as SP

app_name = 'sheet'

urlpatterns = [
    path('', SP.start_check_sheet, name="start_sheet"),
]
