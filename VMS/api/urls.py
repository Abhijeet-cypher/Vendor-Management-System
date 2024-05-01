from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('login/', obtain_jwt_token, name='login'),
    # path('token/', obtain_jwt_token, name='generate_token'),
    # path('vendors/', create_vendor, name='create_vendor'),
    path('vendors/', vendors_list, name='list_vendors'),
    path('vendors/<int:vendor_id>/', retrieve_vendor, name='retrieve_vendor'),
    path('vendors/<int:vendor_id>/update/', update_vendor, name='update_vendor'),
    path('vendors/<int:vendor_id>/delete/', delete_vendor, name='delete_vendor'),
    path('purchase_orders/', purchase_order, name='create_purchase_order'),
    # path('api/purchase_orders/', list_purchase_orders, name='list_purchase_orders'),
    path('purchase_orders/<int:po_id>/', retrieve_purchase_order, name='retrieve_purchase_order'),
    path('purchase_orders/<int:po_id>/update/', update_purchase_order, name='update_purchase_order'),
    path('purchase_orders/<int:po_id>/delete/', delete_purchase_order, name='delete_purchase_order'),
    path('vendors/<int:vendor_id>/performance/', retrieve_vendor_performance, name='retrieve_vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge_purchase_order'),
]
