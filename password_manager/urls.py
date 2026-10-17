from django.urls import path
from .views import (
    signin,
    signup,
    signout,

    home_view,

    add_password_view,
    edit_password_view,
    delete_password_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),

    path('add-password/', add_password_view, name='add_password'),
    path('edit-password/<str:password_id>/', edit_password_view, name='edit_password'),
    path('delete-password/<str:password_id>/', delete_password_view, name='delete_password'),
]