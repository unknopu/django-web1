from django.contrib import admin
from .models import user_model, transaction
# Register your models here.

# admin.site.register(user_model)

class Person(admin.ModelAdmin):
    list_display = ['user_ref_id','fullname','username','email']
    list_editable = ['fullname','username','email']
 
class Transaction_admin(admin.ModelAdmin):
    list_display = ['ref_id','from_user','to_user','amount','transaction_type','is_verify','time_stamp']
    
admin.site.register(user_model, Person)
admin.site.register(transaction, Transaction_admin)
