from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.post_create),
    path('readOne/', views.post_read_one),
    path('', views.post_read_many_user),
    path('readMany/', views.post_read_many_customer),
    path('update/', views.post_update),
    path('delete/<id>', views.post_delete_user),
    path('delete/<id>', views.post_delete),
]
