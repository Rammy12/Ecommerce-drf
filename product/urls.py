from django.urls import path
from . import views

urlpatterns=[
    path('products/',views.get_products,name="Product"),
    path('products/new/',views.new_product,name="new_product"),
    path('products/<str:pk>/',views.get_product,name="get_product_details"),
    path('product/uplode_images/',views.uplodeProduct_images,name="uplodeProduct_images"),
    path('products/<str:pk>/update/',views.update_product,name="update_product"),
    path('products/<str:pk>/delete/',views.delete_product,name="delete_product"),
    path('<str:pk>/review/',views.create_review,name="create_review"),
    path('<str:pk>/review/delete/',views.delete_review,name="delete_review")
]