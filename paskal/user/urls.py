from django.urls import path, re_path
from .views import signup, signin, signout, profile, user_activity, user_edit

app_name = 'user'
urlpatterns = [
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('signout', signout, name='signout'),
    path('edit', user_edit, name='edit'),
    path('<int:id>', profile, name='profile'),
]
