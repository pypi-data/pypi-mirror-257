from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.db import models

from artd_product.models import (
    Tax,
    RootCategory,
    Category,
    Brand,
    Product,
    ProductImage,
    GroupedProduct,
    Image,
)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "percentage",
        "status",
    )
    list_filter = (
        "name",
        "percentage",
        "status",
    )
    search_fields = (
        "name",
        "percentage",
        "status",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    # Create BrandAdmin


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "status",
    )


@admin.register(RootCategory)
class RootCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "partner",
        "status",
        "url_key",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "partner",
        "parent",
        "status",
        "url_key",
    )
    list_filter = (
        "status",
        "parent",
    )
    search_fields = (
        "name",
        "parent__name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "status",
        "url_key",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "brand__name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "external_id",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "external_id",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "image",
        "status",
    )
    list_filter = (
        "product",
        "status",
    )
    search_fields = (
        "product__name",
        "status",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(GroupedProduct)
class GroupedProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "sku",
        "status",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
