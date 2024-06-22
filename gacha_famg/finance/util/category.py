from db.models import Category

from .base import BaseModelFormatter, BaseModelHandler


class CategoryFormatter(BaseModelFormatter):
    @classmethod
    def as_dict(self, obj: Category) -> dict:
        return dict(
            id=obj.id,
            name=obj.name,
            text_color=obj.text_color,
            bg_color=obj.bg_color,
        )


class CategoryHandler(BaseModelHandler):
    class Meta:
        model = Category
        order = "-priority"
        formatter = CategoryFormatter
