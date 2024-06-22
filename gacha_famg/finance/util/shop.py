from db.models import Shop

from .base import BaseModelFormatter, BaseModelHandler


class ShopFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: Shop) -> dict:
        return dict(
            id=obj.id,
            name=obj.name,
            text_color=obj.text_color,
            bg_color=obj.bg_color,
        )


class ShopHandler(BaseModelHandler):
    class Meta:
        model = Shop
        order = "-priority"
        formatter = ShopFormatter
