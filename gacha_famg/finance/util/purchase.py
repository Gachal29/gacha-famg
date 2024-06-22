from datetime import datetime
from django.db.models import QuerySet
from db.models import Receipt, PurchaseItem, PurchaseRecordMonth, Home

from db.util import get_next_year_month
from .base import BaseModelFormatter, BaseModelHandler


class PurchaseRecordMonthHandler:
    def __init__(self, home: Home):
        self.home = home

    def get_period(self, year_month: str = None) -> tuple[datetime, datetime]:
        start_date = None
        end_date = None

        next_year_month = get_next_year_month(year_month)
        try:
            start_date = PurchaseRecordMonth.objects.get(
                home=self.home, year_month=year_month
            ).date
        except PurchaseRecordMonth.DoesNotExist:
            return start_date, end_date
        try:
            end_date = PurchaseRecordMonth.objects.get(
                home=self.home, year_month=next_year_month
            ).date
        except PurchaseRecordMonth.DoesNotExist:
            pass
        return start_date, end_date


class ReceiptFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: Receipt):
        return dict(
            id=obj.id,
            date=obj.date,
            shop_id=obj.shop.id,
        )
    

class ReceiptHandler(BaseModelHandler):
    class Meta:
        model = Receipt
        order = "-date"
        formatter = ReceiptFormatter

    def __init__(self, home: Home, year_month: str):
        super().__init__(home)
        self.year_month = year_month


    def get_queryset(self, force: bool = False) -> QuerySet[Receipt]:
        purchase_record_month_handler = PurchaseRecordMonthHandler(self.home)
        start_date, end_date = purchase_record_month_handler.get_period(year_month=self.year_month)
        model = self.Meta.model
        order = self.Meta.order
        if start_date and end_date:
            self.queryset = model.objects.filter(
                home=self.home,
                date__range=[start_date, end_date],
            ).order_by(order)
        elif start_date and not end_date:
            self.queryset = model.objects.filter(
                home=self.home,
                date__gte=start_date,
            ).order_by(order)
        else:
            self.queryset = model.objects.none()
        return self.queryset
    

class PurchaseItemFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: PurchaseItem):
        return dict(
            id=obj.id,
            receipt_id=obj.receipt.id,
            category_id=obj.category.id,
            detail=obj.detail,
            price=obj.price,
            discount=obj.discount,
            note=obj.note,
        )
    

class PurchaseItemHandler(BaseModelHandler):
    class Meta:
        model = PurchaseItem
        order = "-receipt__date"
        formatter = PurchaseItemFormatter

    def __init__(self, receipts: QuerySet[Receipt]):
        self.receipts = receipts

    def get_queryset(self, force: bool = False) -> QuerySet[PurchaseItem]:
        model = self.Meta.model
        order = self.Meta.order
        self.queryset = model.objects.filter(receipt__in=self.receipts,).order_by(order)
        return self.queryset
