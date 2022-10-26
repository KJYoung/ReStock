from django.urls import include, path
from . import views

app_name = "stockKR"
urlpatterns = [
    path('', views.index, name="index"),
    path('<str:name>', views.stockInfoByName, name="byName")
]