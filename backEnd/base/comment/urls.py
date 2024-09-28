from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.comment_create),
    path('readOne/', views.comment_read_one),
    path('readMany/<id>', views.comment_read_many_post),
    path('', views.comment_read_all),
    path('update/', views.comment_update),
    path('delete/<id>', views.comment_delete),
    path('test/', views.test)
]
