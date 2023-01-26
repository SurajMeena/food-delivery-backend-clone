from django.urls import path
from . import views

urlpatterns = [
 path('signup', views.signup, name='signup'),
 path('login', views.login, name='login'),
 path('insertUserDetails', views.insert_user_details, name='insertUserDetails'),
 path('getRestaurants', views.get_restaurants, name='getRestaurants'),
 path('getRestaurantMenu', views.get_restaurant_menu, name='getRestaurantMenu'),
 path('getOrderHistory', views.get_order_history, name='getOrderHistory'),
 path('getTransactionHistory', views.user_trans_history, name='getTransactionHistory'),
 path('getUserDetails', views.get_user_details, name='getUserDetails'),
 path('updateOrder', views.update_order, name='updateOrder'),
 path('addToCart', views.add_to_cart, name='addToCart'),
 path('removeFromCart', views.remove_from_cart, name='removeFromCart'),
 path('calculateETA', views.calculate_eta, name='calculateETA'),
 path('insertOrderJourney', views.insert_order_journey, name='insertOrderJourney'),
 path('updateOrderJourney', views.update_order_journey, name='updateOrderJourney'),
]