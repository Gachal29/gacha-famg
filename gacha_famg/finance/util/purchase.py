from datetime import datetime, timedelta
from django.db.models import QuerySet
from db.models import Receipt, PurchaseItem, PurchaseRecordMonth, Home

from db.util import get_next_year_month
from .base import BaseModelFormatter, BaseModelHandler


class PurchaseRecordMonthFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: PurchaseRecordMonth):
        year_month_split = obj.year_month.split("_")
        return dict(
            year_month=obj.year_month,
            year_month_text=f"{year_month_split[0]}年{year_month_split[1]}月",
            date=str(obj.date),
        )

class PurchaseRecordMonthHandler(BaseModelHandler):
    class Meta:
        model = PurchaseRecordMonth
        order = "date"
        formatter = PurchaseRecordMonthFormatter

    def get_period(self, year_month: str = None) -> tuple[datetime, datetime]:
        start_date = None
        end_date = None

        next_year_month = get_next_year_month(year_month)
        model = self.Meta.model
        try:
            start_date = model.objects.get(
                home=self.home, year_month=year_month
            ).date
        except model.DoesNotExist:
            return start_date, end_date
        try:
            end_date = model.objects.get(
                home=self.home, year_month=next_year_month
            ).date - timedelta(days=1)
        except model.DoesNotExist:
            pass
        return start_date, end_date


class ReceiptFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: Receipt):
        return dict(
            id=str(obj.id),
            date=str(obj.date),
            shop_id=obj.shop.id,
        )
    

class ReceiptHandler(BaseModelHandler):
    class Meta:
        model = Receipt
        order = "-date"
        formatter = ReceiptFormatter

    def __init__(self, home: Home, start_date: datetime, end_date: datetime):
        super().__init__(home)
        self.start_date = start_date
        self.end_date = end_date

    def get_queryset(self, force: bool = False) -> QuerySet[Receipt]:
        model = self.Meta.model
        order = self.Meta.order
        if self.start_date and self.end_date:
            self.queryset = model.objects.filter(
                home=self.home,
                date__range=[self.start_date, self.end_date],
            ).order_by(order)
        elif self.start_date and not self.end_date:
            self.queryset = model.objects.filter(
                home=self.home,
                date__gte=self.start_date,
            ).order_by(order)
        else:
            self.queryset = model.objects.none()
        return self.queryset
    

class PurchaseItemFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: PurchaseItem):
        return dict(
            id=obj.id,
            receipt_id=str(obj.receipt.id),
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
