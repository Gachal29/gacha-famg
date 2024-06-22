from django.db.models import Model, QuerySet

from db.models import Home


class BaseModelFormatter:
    @classmethod
    def as_dict(self, obj) -> dict:
        return {}


class BaseModelHandler:
    queryset: QuerySet = None

    class Meta:
        model: Model = None
        order: str = None
        formatter: BaseModelFormatter = None

    def __init__(self, home: Home):
        self.home = home

    def get_queryset(self, force: bool=False) -> QuerySet:
        model = self.Meta.model
        if not model:
            raise ValueError("modelを設定してください。")
        if not self.queryset or force:
            try:
                order = self.Meta.order
                self.queryset = model.objects.filter(home=self.home).order_by(order)
            except:
                self.queryset = model.objects.filter(home=self.home)
        return self.queryset

    def as_list(self) -> list[dict]:
        if not self.queryset:
            self.get_queryset()

        try:
            formatter = self.Meta.formatter
            list_data = []
            for obj in self.queryset:
                list_data.append(formatter.as_dict(obj))
            return list_data
        except:
            return list(self.queryset)
