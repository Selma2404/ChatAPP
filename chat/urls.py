
from django.urls import include, path

from . import routing
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('chat/<int:user_id>/', views.chat_room, name='chat_room'),
    path('', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path(r'', include(routing.websocket_urlpatterns)),
]

