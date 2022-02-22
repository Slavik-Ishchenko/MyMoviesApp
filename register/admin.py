from django.contrib import admin
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    model = MyUser
    list_display = ('name', 'email', 'date_of_birth', 'is_notified')
    search_fields = ('name', 'email')


admin.site.register(MyUser, MyUserAdmin)
