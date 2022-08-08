from pydoc import importfile
from django.contrib import admin
from ItemMaster.models import*
# Register your models here.
admin.site.register(Warehouse_Master)
admin.site.register(User_Master)
admin.site.register(Item_Master)
admin.site.register(Stock)