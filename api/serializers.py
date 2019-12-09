from rest_framework import serializers

#使用者收藏
from rest_framework.validators import UniqueTogetherValidator

from .models import Coupon,User,UserFav,UserAccounting

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id','username', 'email', 'last_name', 'password')

class CouponSerializer(serializers.ModelSerializer):

    # image_url = serializers.SerializerMethodField('get_url')
    coupon_img = serializers.ImageField(required=False,max_length=None,
                                     allow_empty_file=True, use_url=True)

    class Meta:
        model = Coupon
        fields = ('coupon_id','coupon_title','coupon_class','coupon_note','coupon_notice','coupon_original_price',
                  'coupon_price','coupon_saving','coupon_img')

class UserFavSerializer(serializers.ModelSerializer):
    #獲取當前使用者是誰
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # 設定validate使一個coupons只能收藏一次
        validators = [
            #只能一個
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'coupons'),
                # message的信息可以自定义
                message="已經收藏"
            )
        ]
        model = UserFav
        # 必填，因為取消收藏時要知道ID，所以ID也是必填
        fields = ("user", "coupons", 'id')

class UserAccountingSerializer(serializers.ModelSerializer):
    #獲取當前使用者是誰
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAccounting
        #必填
        fields = ("user", 'id' , "accounting_data" , "accounting_date" , "accounting_class","accounting_month",
                  "accounting_discount","accounting_coupon_name")
