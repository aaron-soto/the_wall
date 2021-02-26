from django.urls import path     
from . import views

urlpatterns = [
    path('', views.login),
	path('login', views.login),
	path('register', views.register),
	path('process_register', views.process_register),
	path('wall', views.wall),
	path('process_logout', views.process_logout),
	path('process_login', views.process_login),
	path('post_message', views.post_message),
	path('<int:num>/add_comment', views.add_comment),
	path('<int:num>/delete_this_message', views.delete_this_message),


]