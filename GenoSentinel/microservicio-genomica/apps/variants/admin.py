from django.contrib import admin
from .models import GeneticVariant

@admin.register(GeneticVariant)
class GeneticVariantAdmin(admin.ModelAdmin):
    list_display = ('gene', 'chromosome', 'position', 'impact', 'created_at')
    list_filter = ('impact', 'chromosome')
    search_fields = ('gene__symbol', 'chromosome', 'position', 'reference_base', 'alternate_base')
    raw_id_fields = ('gene',)
