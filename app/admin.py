from django.contrib import admin
from app.models import News,Category
# Register your models here.

admin.site.register(News)
admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'newsapi_mapping')
    list_editable = ('newsapi_mapping',)