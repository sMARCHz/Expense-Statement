from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_item', views.add_item, name='add item'),
    path('remove_item', views.remove_item, name='remove item'),
    path('list_statement', views.list_item, name='list statement'),
]