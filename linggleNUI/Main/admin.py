from django.contrib import admin
from models import *
# Register your models here.
class QueryAdmin(admin.ModelAdmin):
  list_display = ('query',)
admin.site.register(Query, QueryAdmin)
