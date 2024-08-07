from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
	path("signin/", views.signin, name="signin"),
	path("signup/", views.signup, name="signup"),
	path("signout/", views.signout, name="signout"),
	path("activate/<uidb64>/<token>", views.activate, name="activate"),
	path("<str:id>/", views.update_details, name="update_details")
]
