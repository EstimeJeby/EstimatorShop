from django.urls import path

from .views import (
    
    ProductDetailView,
   
    PostUpdateView,
    PostDeleteView,
    UserProductListView,
  
   
   
)   
from .import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('user/<str:username>', UserProductListView.as_view(), name='user-posts'),
    path('Product/<int:pk>/', ProductDetailView.as_view(), name='post-detail'),

    path('product/cart',views.cart, name='cart'),
    path('product/checkout',views.checkout, name='checkout'),
    path('update_Item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
    path('post/new/',views.UploadProduct, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
   
]
