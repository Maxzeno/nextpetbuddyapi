from django.urls import path, include
from rest_framework import routers
from api import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()

router.register('user', views.UserViewSet, basename='user')
router.register('address', views.AddressViewSet, basename='address')
router.register('cart', views.OrderItemViewSet, basename='orderitem')
router.register('order', views.OrderViewSet, basename='order')
router.register('product', views.ProductListViewSet, basename='product'),

urlpatterns = [
     path('', include(router.urls)),

     path('paystack-webhook/', views.WebhookVerifyPaystackPayment.as_view(), name='paystack-webhook'),
     path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('pet/', views.PetListView.as_view(), name='pet'),
     path('breed/', views.BreedListView.as_view(), name='breed'),

     path('contact-us/', views.ContactUsCreateView.as_view(), name='contact_us'),
     path('newsletter/', views.EmailCreateView.as_view(), name='newsletter'),

     path('change-password/', views.ChangePasswordView.as_view(),
          name='change_password'),
     path('forgot-password/', views.ForgotPasswordView.as_view(),
          name='forgot_password'),
     path('password-reset/<str:uid>/<str:token>/',
          views.PasswordResetView.as_view(), name='password_reset'),
     path('send-confirm-email/<str:uid>/',
          views.SendConfirmEmailView.as_view(), name='send_confirm_email'),
     path('confirm-email/<str:uid>/<str:token>/',
          views.ConfirmEmailView.as_view(), name='confirm_email'),
     path('auth-user/', views.UserView.as_view(), name='auth_user'),
     
     path('schema/', SpectacularAPIView.as_view(), name='schema'),
     path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
     path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
