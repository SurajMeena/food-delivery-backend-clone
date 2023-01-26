# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DeliveryExecutives(models.Model):
    exec_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_executives'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MenuContent(models.Model):
    menu_content_id = models.AutoField(primary_key=True)
    fk_restaurant = models.ForeignKey('Restaurants', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    price = models.FloatField()
    dish_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_content'


class OrderContent(models.Model):
    order_content_id = models.AutoField(primary_key=True)
    fk_order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    fk_menu = models.ForeignKey(MenuContent, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_content'


class OrderJourney(models.Model):
    journey_id = models.AutoField(primary_key=True)
    fk_exec = models.ForeignKey(DeliveryExecutives, models.DO_NOTHING, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_journey'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    fk_restaurant = models.ForeignKey('Restaurants', models.DO_NOTHING, blank=True, null=True)
    payment_method = models.CharField(max_length=100)
    order_status = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    fk_exec = models.ForeignKey(DeliveryExecutives, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Restaurants(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurants'


class UserDetails(models.Model):
    user_detail_id = models.AutoField(primary_key=True)
    wallet_balance = models.FloatField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    default_payment_method = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=1000)
    fk_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_details'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'


class WalletTransactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    fk_order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=6)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transactions'
