from django.contrib import admin
from . import models


@admin.register(models.Home)
class HomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HomeUser)
class HomeUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PurchaseRecordMonth)
class PurchaseRecordMonthAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    pass
