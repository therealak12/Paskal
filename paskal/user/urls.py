from django.urls import path, re_path
from .views import signup, signin, signout, profile

urlpatterns = [
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('signout', signout, name='signout'),
    path('<int:id>', profile, name='profile')
]
