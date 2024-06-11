from django.contrib import admin
from .models import SuppliesPetProduct, SuppliesPetCategory, SuppliesPetImage, SuppliesPetDiscount, ProductVisit
from django.utils.dateformat import format as date_format

admin.site.register(ProductVisit)


@admin.register(SuppliesPetDiscount)
class SuppliesPetDiscountAdmin(admin.ModelAdmin):
    """
    search_fields (product__title),
    search by title (a field in product model for identifications),
    title equal name for product any record.
    """

    list_display = ("id", "product_title", "discount_price", "created_formatted")
    search_fields = ("product__title",)
    list_filter = ("created",)

    def product_title(self, obj):
        return obj.product.title

    product_title.short_description = 'عنوان محصول'

    def created_formatted(self, obj):
        return date_format(obj.created, 'Y-m-d H:i:s')


class SuppliesPetImageInLine(admin.StackedInline):
    model = SuppliesPetImage


@admin.register(SuppliesPetProduct)
class SuppliesPetProductAdmin(admin.ModelAdmin):
    inlines = [SuppliesPetImageInLine]
    filter = ["category", "list_display"]


@admin.register(SuppliesPetCategory)
class SuppliesPetCategoryAdmin(admin.ModelAdmin):
    list_display = ["admin_image", "title"]
