from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, AccountSearchView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:id>', UserDetailView.as_view(), name='user-detail'),

    path('', AccountSearchView.as_view(), name='account-search'),

]
