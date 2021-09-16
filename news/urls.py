from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('<int:post_id>', views.post, name='post')
]