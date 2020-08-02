from django.contrib import admin
from .models import Item

class ListItAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Item, ListItAdmin)
