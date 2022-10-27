from django.contrib import admin
from . import models

@admin.register(models.krStockElementModel)
class KrStockElementModelAdmin(admin.ModelAdmin):
    """krStockElementModel admin definition"""

    list_display = ("__str__",)

class KrStockElementModelInlineAdmin(admin.TabularInline):
    """KrStockElementModel Inline admin for the stockKR definition"""

    model = models.krStockElementModel
    verbose_name = "KR Stock Daily Element"
    verbose_name_plural = "KR Stock Daily Elements"

@admin.register(models.stockKR)
class StockKRAdmin(admin.ModelAdmin):
    """StockKR admin definition"""
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "category",
                    "short_code",
                    "isin_code",
                    "first_date",
                    "last_date"
                )
            },
        ),
    )
    inlines = (KrStockElementModelInlineAdmin,)
    list_display = ("__str__",)
