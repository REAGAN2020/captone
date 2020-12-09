from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # Your URLs...
    path('api/profile/<id>', views.ProfileView.as_view(), name="profile"),
    path('api/user/', views.UserView.as_view(), name="user"),
    path('api/userprofiles', views.ProfilesView.as_view(), name="userprofiles"),
    path('api/profile',views.ProfileIdView.as_view(), name="userprofile"),
    path('api/updateprofile',views.UpdateProfileView.as_view(), name="updateprofile"),
    path('api/<id>/bookcar/', views.BookCar.as_view()),
    path('api/newcar/', views.CreateCarView.as_view(), name="newcar"),
    path('api/cars/', views.CarAllView.as_view(), name="all-cars"),
    path('api/smallcars/', views.SmallCarCategoryView.as_view(), name="small cars"),
    path('api/midcars/', views.MidCarCategoryView.as_view(), name="small cars"),
    path('api/largecars/', views.LargeCarCategoryView.as_view(), name="small cars"),
    path('api/ambulance/', views.AmbulanceCarCategoryView.as_view(), name="small cars"),
    path('api/car/<id>', views.CarIdView.as_view(), name="car"),
    path('api/deletecar/<id>', views.CarDeleteView.as_view(), name="car"),
    path('api/bookings', views.UserBookingsView.as_view(), name="booking"),

]
urlpatterns = format_suffix_patterns(urlpatterns)


