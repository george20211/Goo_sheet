from django.urls import path, include

urlpatterns = [
    path('', include("google_sheet.urls")),
]
