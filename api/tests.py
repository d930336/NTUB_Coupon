from django.test import TestCase
from api.models import User , Coupon , UserAccounting

from rest_framework import status
from rest_framework.test import APITestCase

#Django Model Test
class UserModelTestCase(TestCase):

    def test_create_user(self):
        user = User(username="jack")
        user.save()
        db_user = User.objects.get(username=user.username)
        self.assertEqual(user == db_user , True)

    def test_create_coupon(self):
        coupon = Coupon(coupon_id = "655" , coupon_price = 87 , coupon_original_price = 107 , coupon_title = "測試"
                        ,coupon_class = "食物" , coupon_note = "測試" , coupon_notice ="測試" , coupon_saving = 20)
        coupon.save()
        db_coupon = Coupon.objects.get(coupon_id = coupon.coupon_id)
        self.assertEqual(coupon == db_coupon , True)

    def test_create_useraccounting(self):
        user = User(username="jack2")
        user.save()

        useraccounting = UserAccounting(user_id=user.id,accounting_class='食物',accounting_data=111,accounting_date='1110',accounting_discount='八折'
                       ,accounting_coupon_name='優惠卷測試',accounting_month='11')
        useraccounting.save()
        db_useraccounting = UserAccounting.objects.get(user_id = user.id)
        self.assertEqual(useraccounting == db_useraccounting, True)

#API Test
class AccountTests(APITestCase):
    def test_create_account(self):
        url = '/rest-auth/registration/'
        data = {'username': 'benson','email':'aa@bb.cc', 'password1':'as12345678' , 'password2':'as12345678'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'benson')
    def test_email_confirm(self):
        url = "/api-token-auth/"
        data = {"username":"benson" , "password":"as12345678"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

