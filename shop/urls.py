from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_view,{'category_name' : None}, name='shop'),
    path('product/<int:pk>/', views.product_description, name='product_description'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('category/<str:category_name>/', views.shop_view, name='category_view'),
    path('cart/', views.my_cart_view, name='my_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('billing/', views.billing_view, name='billing'),
    path('myorder/', views.myorder_list_view, name='myorder_list'),
    path('myorder/<int:order_id>/', views.myorder_view, name='myorder'),
    path('track/', views.track_order_view, name='track_order'),

]
