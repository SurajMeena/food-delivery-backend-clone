from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from ..models import *
from icecream import ic
from django.utils import timezone
from .utilities import *
from datetime import datetime



ic.configureOutput(includeContext=True)


# APIs built using Django REST framework
@api_view(["POST"])
def signup(request):
    try:
        email = request.data["email"]
        pwd = request.data["password"]
        user = Users.objects.get(email=email)
        return JsonResponse(
            {"message": "User already registered"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        user_data = Users.objects.create(
            email=email, password=pwd, created_at=timezone.now()
        )
        ic(user_data.user_id)
        request.session["user_id"] = user_data.user_id
        return JsonResponse({"message": "User Created Successfully"})
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def login(request):
    email = request.data["email"]
    pwd = request.data["password"]
    try:
        user = Users.objects.get(email=email, password=pwd)
        request.session["user_id"] = user.user_id
        # update last login in user_details table
        user_details = UserDetails.objects.get(fk_user=user)
        user_details.last_login = timezone.now()
        user_details.save()
        return JsonResponse({"message": "User Logged In Successfully"})
    except Users.DoesNotExist:
        return JsonResponse({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def insert_user_details(request):
    try:
        expiry_time = request.session.get_expiry_date()
        # Check if the token exists and is valid
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        # Check if the token has expired
        if timezone.now() > expiry_time:
            return JsonResponse({"message": "Session Token Expired"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        wallet_balance = 0
        default_payment_method = request.data["defaultPaymentMethod"]
        latitude = request.data["latitude"]
        longitude = request.data["longitude"]
        address = request.data["address"]
        user_data = UserDetails.objects.create(
            wallet_balance=wallet_balance,
            default_payment_method=default_payment_method,
            address=address,
            latitude=latitude,
            longitude=longitude,
            fk_user_id=user_id,
        )
        return JsonResponse({"message": "User Details Added Successfully"})
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_restaurants(request):
    try:
        restaurants = Restaurants.objects.values()
        return JsonResponse(
            {
                "message": "Restaurants Fetched Successfully",
                "restaurants": list(restaurants),
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_restaurant_menu(request):
    try:
        restaurant_id = request.GET.get("restaurantID")
        restaurant = Restaurants.objects.get(pk=restaurant_id)
        menu = MenuContent.objects.filter(fk_restaurant_id=restaurant_id).values()
        return JsonResponse(
            {
                "message": "Menu Fetched Successfully",
                "restaurant_name": restaurant.name,
                "menu" : list(menu)
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_order_history(request):
    try:
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        orders = Orders.objects.filter(fk_user_id=user_id).values()
        order_list = []
        for order in orders:
            restaurant = Restaurants.objects.get(pk=order.get('fk_restaurant_id'))
            order_items = OrderContent.objects.filter(fk_order_id=order.get('id')).values()
            order_list.append({
                "order_id": order.get('id'),
                "restaurant_name": restaurant.name,
                "items": list(order_items)
            })
        return JsonResponse(
            {
                "message": "Orders Fetched Successfully",
                "orders": order_list,
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# TODO: get order details that is menu along with prices and total amount
# take ispiration from swiggy app
# @api_view(["GET"])
# def get_order_details(request):


@api_view(["GET"])
def user_trans_history(request):
    try:
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        wallet_transactions = WalletTransactions.objects.filter(fk_user_id=user_id).values()
        return JsonResponse(
            {
                "message": "Wallet Transactions Fetched Successfully",
                "walletTransactions": list(wallet_transactions),
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def order_trans_history(request):
    try:
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        order_id = request.GET.get("orderID")
        wallet_transactions = WalletTransactions.objects.filter(fk_user_id=user_id, fk_order_id=order_id)
        return JsonResponse(
            {
                "message": "Wallet Transactions Fetched Successfully",
                "walletTransactions": list(wallet_transactions),
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_user_details(request):
    try:
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        user_details = UserDetails.objects.filter(fk_user_id=user_id).values()
        return JsonResponse(
            {
                "message": "User Details Fetched Successfully",
                "userDetails": list(user_details),
            }
        )
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def push_order(request):
    try:
        if not request.session.session_key:
            return JsonResponse({"message": "Invalid or Expired Session"}, status=status.HTTP_401_UNAUTHORIZED)
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        payment_method = request.data["paymentMethod"]
        restaurant_id = request.data["restaurantID"]
        total_amount = request.data["totalAmount"]
        order = Orders.objects.create(
            order_total=total_amount,
            fk_user_id=user_id,
            payment_method=payment_method,
            fk_restaurant_id=restaurant_id,
            order_status="inCart",
            created_at=timezone.now(),
        )
        order_id = order.order_id
        ic(order_id)
        items = request.data["items"]
        for item in items:
            ic(item)
            item_id = item["itemID"]
            quantity = item["quantity"]
            price = item["price"]
            item_instance = MenuContent.objects.get(pk=item_id)
            OrderContent.objects.create(
                fk_order=order,
                fk_menu=item_instance,
                quantity=quantity,
            )
        return JsonResponse({"message": "Order Added Successfully"})
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def update_order_status(request):
    try:
        order_id = request.data["orderID"]
        order_status = request.data["orderStatus"]
        order = Orders.objects.get(pk=order_id)
        order.order_status = order_status
        order.save()
        return JsonResponse({"message": "Order Updated Successfully"})
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# @api_view(["POST"])
#     user = authenticate(username='john', password='secret')
#     if user is not None:
