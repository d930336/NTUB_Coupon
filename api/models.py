from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True,verbose_name="建立時間")
    gender=models.CharField(max_length=1,verbose_name="性別")
    email = models.EmailField(unique=True,verbose_name = '信箱')
    REQUIRED_FIELDS = ["gender","email"]

    class Meta:
        verbose_name = '使用者'
        verbose_name_plural = verbose_name
        ordering = ('created',)

class Coupon(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon_id = models.CharField(max_length=20, primary_key=True,verbose_name="優惠卷編號")
    coupon_price = models.IntegerField(verbose_name="優惠卷特價價格")
    coupon_original_price = models.IntegerField(blank=True,null=True,verbose_name="優惠卷原始價格")
    coupon_title = models.CharField(max_length=150,verbose_name="優惠卷標題")
    coupon_class = models.CharField(max_length=20,verbose_name="優惠卷類別")
    coupon_note = models.CharField(max_length=200,verbose_name="優惠卷內容")
    coupon_notice = models.CharField(max_length=200,verbose_name="優惠卷注意事項")
    coupon_saving = models.IntegerField(verbose_name="優惠卷折扣")
    coupon_img = models.ImageField(upload_to='coupons', blank=True,null=True,verbose_name="優惠卷圖片")
    coupon_create_at = models.DateTimeField(auto_now_add=True,verbose_name="優惠卷創建時間")

    class Meta:
        verbose_name = '優惠卷'
        verbose_name_plural = verbose_name
        ordering = ('coupon_create_at',)

    def __str__(self):
        return self.coupon_title

#使用者收藏
class UserFav(models.Model):

    #兩個外鍵行成關聯表
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="使用者")
    coupons = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name="優惠卷", help_text="優惠卷id")
    user_fav_create_at = models.DateTimeField("添加時間",auto_now_add=True)

    class Meta:
        verbose_name = '使用者收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "coupons")

    def __str__(self):
        return self.user.username

#使用者記帳
class UserAccounting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="使用者")
    accounting_class = models.CharField(max_length=30,verbose_name="記帳類別")
    accounting_data  = models.IntegerField(default=0,verbose_name="記帳資料")
    accounting_date = models.CharField(max_length=30 , default=str(datetime.datetime.now().strftime("%m%d")),
                                       verbose_name="記帳日期")
    accounting_discount = models.CharField(max_length=30,blank=True,null=True,verbose_name="記帳折扣")
    accounting_coupon_name = models.CharField(max_length=50,blank=True,null=True,verbose_name="優惠卷名稱")
    accounting_month = models.CharField(max_length=2,verbose_name="記帳月份")
    user_accounting_post_at = models.DateTimeField(auto_now_add=True,verbose_name="記帳創建時間")

    class Meta:
        verbose_name = '使用者記帳'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
