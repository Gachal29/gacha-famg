from django.contrib import admin, messages

from .importer import FinanceExcelImporter
from . import models


@admin.register(models.ImportPurchaseRecordFile)
class ImportPurchaseRecordFileAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        """保存を行わずにファイルインポートを実行する
        """

        importer = FinanceExcelImporter(
            obj.home,
            obj.year_month,
            obj.date,
            obj.file.file,
        )
        purchase_record_month_created, shop_created, category_created = importer.import_from_file()
        msg_list = []
        if purchase_record_month_created:
            msg_list.append("購入記録の月管理を作成しました。")
        msg_list.append(f"{shop_created}件のショップと{category_created}件のカテゴリを新規作成しました。")
        self.message_user(
            request,
            "".join(msg_list),
            messages.SUCCESS
        )
