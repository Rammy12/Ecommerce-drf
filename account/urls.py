from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register,name="register"),
    path('me/',views.current_user,name="current_user"),
    path('me/update/',views.update_user,name="update_user"),
    path('forget_password/',views.forget_password,name="forget_password"),
    path('reset_password/<str:token>',views.reset_password,name="reset_password"),
    path('uplodeProfile/',views.uplode_profile_image,name="uplode_profile_image")
]