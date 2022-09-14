from django.contrib import admin
from django.urls import path
from ItemMaster import views

app_name = "ItemMaster"

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('display/', views.display, name='display'), 
    path('Login_change_psw/', views.Login_change_psw, name='Login_change_psw'), 
    path('itemedit/<int:pk>/', views.itemedit, name='itemedit'),
    path('itemdelete/<int:pk>/', views.delete_data, name='itemdelete'),
    # path('', views.warehouse, name='warehouse'), 
    path('warehouseshow/', views.warehouseshow, name='warehouseshow'),
    path('addwarehouse/', views.warehouse, name='addwarehouse') ,
    path('warehouse_edit/<int:pk>/', views.warehouse_edit, name='warehouse_edit') ,
    path('delete_warehouse/<int:pk>', views.delete_warehouse, name='delete_warehouse'),
    path('user/', views.user, name='user'),
    path('user_data/', views.user_data, name='user_data'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit') ,
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('Stock_Add/<int:pk>', views.Stock_Add, name='Stock_Add'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    # path('weekreportpdf/', views.weekreportpdf, name='weekreportpdf'),
    path('Add_Payment_Master/<int:pk>', views.Add_Payment_Master, name='Add_Payment_Master'),
    path('Payment_Master/', views.Payment_Master, name='Payment_Master'),
    path('Payment_Details/<int:pk>', views.Payment_Details, name='Payment_Details'),
    path('Edit_Payment/<int:pk>', views.Edit_Payment, name='Edit_Payment'),
    path('Payment_Delete/<int:pk>', views.Payment_Delete, name='Payment_Delete'),

    path('invoice_file/',views.invoice_file, name= "invoice_file"),
    path('create_invoice/',views.create_invoice, name= "create_invoice"),
    path('Invoice_view/',views.Invoice_view, name= "Invoice_view"),
    path('delete_invoice/<int:pk>',views.delete_invoice, name= "delete_invoice"),
    path('Invoice_Edit/<int:pk>',views.Invoice_Edit, name= "Invoice_Edit"),
    path('Invoice_item_del/<int:pk>',views.Invoice_item_del, name= "Invoice_item_del"),
    path('get_items_ajax/',views.get_items_ajax, name= "get_items_ajax"),
    path('get_dealer_ajax/',views.get_dealer_ajax, name= "get_dealer_ajax"),
    path('Create_Purchase_Order/',views.Create_Purchase_Order, name= "Create_Purchase_Order"),
    path('Purchase_Order/', views.Purchase_Order, name='Purchase_Order'),
    path('Purchase_Items/', views.Purchase_Items, name='Purchase_Items'),
    path('Edit_Purchase_Order/<int:pk>',views.Edit_Purchase_Order, name= "Edit_Purchase_Order"),
    path('Po_item_del/<int:pk>',views.Po_item_del, name= "Po_item_del"),
    path('Purchase_Order_cancle/<int:pk>',views.Purchase_Order_cancle, name= "Purchase_Order_cancle"),
    path('purchace_order_pdf_view/<int:pk>',views.purchace_order_pdf_view, name= "purchace_order_pdf_view"),
    path('Invoice_Pdf/<int:pk>',views.Invoice_Pdf, name= "Invoice_Pdf"),
    
    # path('del_user/',views.del_user, name= "del_user"),
    # path('generateinvoice/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('weekreportpdf/', views.weekreportpdf, name="weekreportpdf"),
    path('ry/', views.ry, name='ry'),



    # reports
    path('invoice_summery_by_month/',views.invoice_summery_by_month, name= "invoice_summery_by_month"),
    path('dealer_summery_by_month/',views.dealer_summery_by_month, name= "dealer_summery_by_month"),
    path('Payment_Satus_per_invoice/',views.Payment_Satus_per_invoice, name= "Payment_Satus_per_invoice"),
    path('ledger/',views.ledger, name= "ledger"),
    path('stock_model_wise/',views.stock_model_wise, name= "stock_model_wise"),
    path('vehicle/',views.vehicle, name= "vehicle"), 
    path('transactions/',views.transactions,name="transactions"),
    path('item_report/',views.item_report,name="item_report"),
    path('profit_loss/',views.profit_loss,name="profit_loss"),
    path('warehouseWise_stock/',views.warehouseWise_stock,name="warehouseWise_stock"),
    path('item_report_ajex/',views.item_report_ajex,name="item_report_ajex"),
    path('low_stock/',views.low_stock,name="low_stock"),
    path('day_wise_saleitem/',views.day_wise_saleitem,name="day_wise_saleitem"),
    
    
    # credit note
    path('creditnote_view/', views.creditnote_view, name='creditnote_view'),     
    path('creditnote_add/', views.creditnote_add, name='creditnote_add'),
    path('dealersinvoice/', views.dealersinvoice, name='dealersinvoice'),
    path('get_invoice_data/', views.get_invoice_data, name='get_invoice_data'),
    path('delete_credit_items/',views.delete_credit_items, name= "delete_credit_items"),
    path('add_credit_items/',views.add_credit_items, name= "add_credit_items"),
    path('select_credit_note/<int:id>',views.select_credit_note, name= "select_credit_note"),
    path('edit_credit_note/<int:id>',views.edit_credit_note, name= "edit_credit_note"),
    path('cancel_credit_listitem/<int:id>',views.cancel_credit_listitem, name= "cancel_credit_listitem"),
    path('delete_credit_selecteditem/<int:id>',views.delete_credit_selecteditem, name= "delete_credit_selecteditem"),
    
  
] 

