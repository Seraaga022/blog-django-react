from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.draft_create),
    path('readOne/', views.draft_read_one),
    path('readMany/', views.draft_read_many),
    path('', views.draft_read_many_user),
    path('update/', views.draft_update),
    path('delete/<id>', views.draft_delete),
    path('publish/', views.draft_publish),
]
