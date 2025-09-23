from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('librarian/signup/', views.librarian_signup, name='librarian_signup'),
    path('login/', views.login_view, name='login'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
