from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('validate_otp/',views.validate_otp,name='validate_otp'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('update_password/',views.update_password,name='update_password'),
    path('change_password/',views.change_password,name='change_password'),
    path('add_book/',views.add_book,name='add_book'),
    path('view_book/',views.view_book,name='view_book'),
    path('seller_index/',views.seller_index,name='seller_index'),
    path('book_detail/<int:pk>/',views.book_detail,name='book_detail'),
    path('stock_availability/<int:pk>/',views.stock_availability,name='stock_availability'),
    path('book_delete/<int:pk>/',views.book_delete,name='book_delete'),
    path('book_edit/<int:pk>/',views.book_edit,name='book_edit'),
    path('unavailable_books/',views.unavailable_books,name='unavailable_books'),
    path('available_books/',views.available_books,name='available_books'),
    path('search_book',views.search_book,name='search_book'),
    path('show_book/<str:bn>/',views.show_book,name='show_book'),
    path('user_book_detail/<int:pk>/',views.user_book_detail,name='user_book_detail'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('mywishlist/',views.mywishlist,name='mywishlist'),
    path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('mycart/',views.mycart,name='mycart'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('move_to_cart/<int:pk>/',views.move_to_cart,name='move_to_cart'),
    path('move_to_wishlist/<int:pk>/',views.move_to_wishlist,name='move_to_wishlist'),
    path('profile/',views.profile,name='profile'),
    path('update_price/',views.update_price,name='update_price'),
]