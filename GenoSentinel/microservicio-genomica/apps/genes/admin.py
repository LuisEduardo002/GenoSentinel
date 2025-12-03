from django.contrib import admin
from .models import Gene

@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'full_name', 'created_at')
    search_fields = ('symbol', 'full_name', 'function_summary')
    list_filter = ('created_at', 'updated_at')
