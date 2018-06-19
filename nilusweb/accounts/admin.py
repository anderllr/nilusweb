from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserAdminCreationForm,UserAdminForm
# Register your models here.


class UserAdmin(BaseUserAdmin):


   add_form = UserAdminCreationForm
   add_fieldsets = (
       (None, {
           'fields': ('username', 'email', 'password1', 'password2')
       }),
   )
   form = UserAdminForm
   fieldsets = (
       (None,{
           'fields' :('username','email','img_user')
       }),
       ('Informações Básicas',{
           'fields' :('name','last_login','qtd_users','qtd_unity','user_master','conta_presente')
       }),
       ('Permissões', {
           'fields': (
               'is_active','is_staff','is_superuser','is_masteruser','groups','user_permissions'
           )
       }),

   )
   list_display = ['username','name','email','img_user','is_active','is_staff','date_joined','is_masteruser','conta_presente']




admin.site.register(User,UserAdmin)


