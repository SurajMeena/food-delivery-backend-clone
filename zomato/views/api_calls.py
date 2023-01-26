from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from icecream import ic
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from ..serializers import *
from geopy.distance import geodesic

ic.configureOutput(includeContext=True)


# APIs built using Django REST framework
@swagger_auto_schema(
    method="post",
    request_body=UsersSerializer,
    operation_description="Create a new user",
)
@api_view(["POST"])
def signup(request):
    try:
        email = request.data["email"]
        pwd = request.data["password"]
        # check if user already exists
        user = Users.objects.get(email=email)
        return JsonResponse(
            {"message": "User already registered"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Users.DoesNotExist:
        # new user
        user_data = Users.objects.create(
            email=email, password=pwd, created_at=timezone.now()
        )
        # create a session for the user
        request.session["user_id"] = user_data.user_id
        return JsonResponse({"message": "User Created Successfully"})
    except Exception as e:
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
        return JsonResponse(
            {"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def insert_user_details(request):
    '''This function is used to insert the user details into the database.'''
    try:
        expiry_time = request.session.get_expiry_date()
        # Check if the token exists and is valid
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if the token has expired
        if timezone.now() > expiry_time:
            return JsonResponse(
                {"message": "Session Token Expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
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
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_restaurants(request):
    '''Returns:A list of restaurants.'''
    try:
        restaurants = Restaurants.objects.values()
        return JsonResponse(
            {
                "message": "Restaurants Fetched Successfully",
                "restaurants": list(restaurants),
            }
        )
    except Exception as e:
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
                "menu": list(menu),
            }
        )
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_order_history(request):
    '''Returns the order history of the user with items and their corresponding price.'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # extending session expiry time
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        orders = Orders.objects.filter(fk_user_id=user_id)
        order_list = []
        for order in orders:
            order_items = OrderContent.objects.filter(
                fk_order_id=order.order_id
            ).values("fk_menu_id", "quantity")
            ic(list(order_items))
            restrau_details = Restaurants.objects.filter(
                pk=order.fk_restaurant_id
            ).values("name")
            # append price, quantity and name of the item to the items list
            items = []
            for item in order_items:
                temp_dict = {}
                temp_dict["price"] = MenuContent.objects.get(
                    pk=item["fk_menu_id"]
                ).price
                temp_dict["quantity"] = item["quantity"]
                temp_dict["name"] = MenuContent.objects.get(
                    pk=item["fk_menu_id"]
                ).name
                items.append(temp_dict)
            order_list.append(
                {
                    "order_id": order.order_id,
                    "restaurant_name": restrau_details[0]["name"],
                    "items": items,
                    "delivery_executive": order.fk_exec_id,
                }
            )
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


@api_view(["GET"])
def user_trans_history(request):
    '''Returns the transaction history of the user.'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        wallet_transactions = WalletTransactions.objects.filter(
            fk_user_id=user_id
        ).values()
        return JsonResponse(
            {
                "message": "Wallet Transactions Fetched Successfully",
                "walletTransactions": list(wallet_transactions),
            }
        )
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def order_trans_history(request):
    '''Returns the transaction history for an order of a user.'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        order_id = request.GET.get("orderID")
        wallet_transactions = WalletTransactions.objects.filter(
            fk_user_id=user_id, fk_order_id=order_id
        )
        return JsonResponse(
            {
                "message": "Wallet Transactions Fetched Successfully",
                "walletTransactions": list(wallet_transactions),
            }
        )
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_user_details(request):
    '''Returns details of the user.'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
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
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def update_order(request):
    '''Updates the order status and payment method.
    
    if order status is being set to inProgress, that is order has been placed and the payment has been made.

    Parameters:
    orderID (int): order id of the order not required if order is currently in cart
    orderStatus (string): can take values "inProgress", "delivered", "cancelled"
    paymentMethod (string): mode of payment only required if orderStatus is "inProgress"
    '''
    try:
        order_status = request.data["orderStatus"]
        order_id = request.data.get("orderID", None)
        payment_method = request.data.get("paymentMethod", None)
        if order_status == "inProgress" and payment_method is None:
            return JsonResponse(
                {"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.session.has_key("order_id"):
            order_id = request.session["order_id"]
        order = Orders.objects.get(pk=order_id)
        order.order_status = order_status
        # only runs when an order is moved from cart to placing order
        if payment_method is not None and order_status == "inProgress":
            delivery_executive = DeliveryExecutives.objects.order_by("?").first()
            order.fk_exec_id = delivery_executive
            order.payment_method = payment_method
            del request.session["order_id"]
        order.save()
        return JsonResponse({"message": "Order Updated Successfully"})
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def add_to_cart(request):
    '''Adds an item to the cart. If the cart doesn't exist then creates a new order with status "inCart"
     and adds the item to that order.'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        restaurant_id = request.data["restaurantID"]
        item_id = request.data["itemID"]
        # check whether cart exists or not
        if not request.session.has_key("order_id"):
        # create an order if cart doesn't exist
            order = Orders.objects.create(
                fk_user_id=user_id,
                fk_restaurant_id=restaurant_id,
                order_status="inCart",
                created_at=timezone.now(),
            )
            request.session["order_id"] = order.order_id
        order_id = request.session["order_id"]
        # increment quantity if item already exists in cart
        if OrderContent.objects.filter(
            fk_order_id=order_id, fk_menu_id=item_id
        ).exists():
            order_content = OrderContent.objects.get(
                fk_order_id=order_id, fk_menu_id=item_id
            )
            order_content.quantity += 1
        else:
            # else add a new item to the cart
            order_content = OrderContent.objects.create(
                fk_order_id=order_id,
                fk_menu_id=item_id,
                quantity=1,
            )
        order_content.save()
        return JsonResponse({"message": "Item Added to Cart Successfully"})
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def remove_from_cart(request):
    '''removes an item from the cart. If the cart is empty then deletes the order with status "inCart"'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        item_id = request.data["itemID"]
        order_id = request.session.get("order_id")
        order_content = OrderContent.objects.get(
            fk_order_id=order_id, fk_menu_id=item_id
        )
        order_content.quantity -= 1
        if order_content.quantity == 0:
            order_content.delete()
            order = Orders.objects.get(pk=order_id)
            order.delete()
            del request.session["order_id"]
        order_content.save()
        return JsonResponse({"message": "Item Removed from Cart Successfully"})
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def calculate_eta(request):
    '''Calculates the estimated time of arrival of the order
    
    if fromRestaurant is true then calculates the ETA from the restaurant to the user
    else calculates the ETA from the delivery executive to the user
    '''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        order_id = request.data["orderID"]
        from_restaurant = request.data["fromRestaurant"]
        order = Orders.objects.get(pk=order_id)
        user_detail = UserDetails.objects.get(fk_user=user_id)
        restaurant = Restaurants.objects.get(pk=order.fk_restaurant_id)
        order_journey = OrderJourney.objects.get(fk_order_id=order_id)
        if from_restaurant == 'true':
            order_latitude = restaurant.latitude
            order_longitude = restaurant.longitude
        else:
            order_latitude = order_journey.latitude
            order_longitude = order_journey.longitude
        user_latitude = user_detail.latitude
        user_longitude = user_detail.longitude
        distance = geodesic(
            (order_latitude, order_longitude), (user_latitude, user_longitude)
        ).km
        eta = distance / 0.5
        return JsonResponse({"message": "ETA Calculated Successfully", "eta": round(eta/60)})
    except Exception as e:
        ic(e)
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def insert_order_journey(request):
    '''inserts the order journey when delivery executive reaches the restaurant'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        order_id = request.data["orderID"]
        exec_id = request.data["execID"]
        latitude = request.data["latitude"]
        longitude = request.data["longitude"]
        order = Orders.objects.get(pk=order_id)
        order_journey = OrderJourney.objects.create(
            fk_order=order,
            latitude=latitude,
            longitude=longitude,
            fk_exec_id=exec_id,
            last_updated=timezone.now(),
        )
        order_journey.save()
        return JsonResponse({"message": "Delivery Partner reached restaurant successfully"})
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def update_order_journey(request):
    '''updates the order journey based on delivery executive's location'''
    try:
        if not request.session.session_key:
            return JsonResponse(
                {"message": "Invalid or Expired Session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.session.set_expiry(300)
        user_id = request.session["user_id"]
        order_id = request.data["orderID"]
        latitude = request.data["latitude"]
        longitude = request.data["longitude"]
        order_journey = OrderJourney.objects.get(fk_order_id=order_id)
        order_journey.latitude = latitude
        order_journey.longitude = longitude
        order_journey.last_updated = timezone.now()
        order_journey.save()
        return JsonResponse({"message": "Delivery Partner location updated successfully"})
    except Exception as e:
        return JsonResponse(
            {"message": "Oops some error occured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )