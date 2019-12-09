from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from api.views import (CouponViewSet,
                              UserViewSet,
                              UserFavViewset,
                              ActivateUserByGet,
                              ResetPasswordUserByGet,
                              UserAccountingViewset, )
#rest_auth
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from django.views.generic import TemplateView

# JWT
from api.views import ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

# rest auth google
from api.views import GoogleLogin

router = DefaultRouter()
router.register(r'coupon',CouponViewSet,base_name='coupon')
router.register(r'users',UserViewSet,base_name='users')
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'useraccouting', UserAccountingViewset, base_name="useraccouting")

urlpatterns = [
    # rest-auth setting /  Registration

    ##-------------------------rest-auth登入----------------------------------------------------------
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
      name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
      name='rest_password_reset_confirm'),
    url(r'^users/login/$', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^users/logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
      name='rest_password_change'),
    ##-------------------------rest-auth登入----------------------------------------------------------

    #因為rest-auth預設使用allauth，所以要匯入allauth的url，才不會造成NoReverse的錯誤
    url(r'^accounts/', include('allauth.urls')),
    #reset password 預設會用到django的admin管理網站，所以我們先匯入他測試看看
    url(r'^', include('django.contrib.auth.urls')),

    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    path("",include(router.urls)),

    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),

    #JWT 套用
    path('api-token-auth/', ObtainJSONWebToken.as_view()),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)