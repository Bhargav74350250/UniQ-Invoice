from pydoc import importfile
from django.contrib import admin
from ItemMaster.models import*
# Register your models here.
admin.site.register(Warehouse_Master)
admin.site.register(User_Master)
admin.site.register(Item_Master)
admin.site.register(Stock)
admin.site.register(INVOICE_MASTER)
admin.site.register(INVOICE_DETAILS)
admin.site.register(PAYMENT_MASTER)
admin.site.register(PAYMENT_STATUS_MASTER)
