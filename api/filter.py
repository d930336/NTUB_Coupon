import django_filters

from .models import Coupon

class CouponFilter(django_filters.rest_framework.FilterSet):
    #field_name -> 要被過濾的東西                lookup -> 要如何過濾(這裡是小於等於)
    price_min = django_filters.NumberFilter(field_name="coupon_price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="coupon_price", lookup_expr='lte')

    class Meta:
        #和serializers的寫法一樣
        model = Coupon
        fields = ['price_min', 'price_max']

