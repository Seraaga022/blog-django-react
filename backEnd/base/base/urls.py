from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.ok_view),
    path('users/', include('user.urls')),
    path('posts/', include('post.urls')),
    path('comments/', include('comment.urls')),
    path('drafts/', include('draft.urls')),
]