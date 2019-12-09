from django.contrib import admin
from .models import User, Coupon , UserFav ,UserAccounting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username' , 'gender' , 'is_superuser' , 'is_active' , 'email')
    search_fields = ('pk', 'username')
    list_filter = ('is_superuser', 'is_active')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_id', 'coupon_title' , 'coupon_original_price' , 'coupon_price' , 'coupon_class' , 'coupon_img')
    search_fields = ('coupon_id', 'coupon_title')
    ordering = ('coupon_id',)

@admin.register(UserFav)
class UserFavAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupons' , 'user_fav_create_at' )
    search_fields = ('user', 'coupons')

@admin.register(UserAccounting)
class UserAccountingAdmin(admin.ModelAdmin):
    list_display = ('user', 'accounting_class', 'accounting_data' , 'accounting_coupon_name'
                    , 'accounting_discount' , 'user_accounting_post_at')
    search_fields = ('user', 'accounting_class' , 'accounting_coupon_name')
    ordering = ('user','-user_accounting_post_at',)

