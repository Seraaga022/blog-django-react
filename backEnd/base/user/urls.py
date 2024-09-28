from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.handle_login, name='login-customer'),
    path('loginUser/', views.handle_login_user, name='login-user'),
    path('signup/', views.handle_signup, name='signup'),
    path('update/', views.update_user, name='update-customer'),
    path('<user_id>', views.user_update_user, name='update-user'),
    path('delete/<id>', views.user_delete, name='delete'),
    path('getOne/<id>', views.get_one_user, name='getone'),
    path('', views.get_all_user, name='get-all'),
]
