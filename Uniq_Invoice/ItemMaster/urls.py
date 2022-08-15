from django.contrib import admin
from django.urls import path
from ItemMaster import views

app_name = "ItemMaster"

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('display/', views.display, name='display'), 
    path('itemedit/<int:pk>/', views.itemedit, name='itemedit'),
    path('itemdelete/<int:pk>/', views.delete_data, name='itemdelete'),
    # path('', views.warehouse, name='warehouse'), 
    path('warehouseshow/', views.warehouseshow, name='warehouseshow'),
    path('addwarehouse/', views.warehouse, name='addwarehouse') ,
    path('warehouse_edit/<int:pk>/', views.warehouse_edit, name='warehouse_edit') ,
    path('delete_warehouse/<int:pk>/', views.delete_warehouse, name='delete_warehouse'),
    path('user/', views.user, name='user'),
    path('user_data/', views.user_data, name='user_data'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit') ,
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('Stock_Add/<int:pk>', views.Stock_Add, name='Stock_Add'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('weekreportpdf/', views.weekreportpdf, name='weekreportpdf'),
    path('Add_Payment_Master/<int:pk>', views.Add_Payment_Master, name='Add_Payment_Master'),
    path('Payment_Master/', views.Payment_Master, name='Payment_Master'),
    path('Payment_Details/', views.Payment_Details, name='Payment_Details'),
    # path('generateinvoice/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    # path('invoice/', views.invoice, name="invoice"),
    path('ry/', views.ry, name='ry'),
  
] 

