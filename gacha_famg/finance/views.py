from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from db.util import default_year_month

from .util.shop import ShopHandler
from .util.category import CategoryHandler
from .util.purchase import ReceiptHandler, PurchaseItemHandler


class TopView(LoginRequiredMixin, TemplateView):
    template_name = "finance/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home = self.request.home
        shop_handler = ShopHandler(home)
        category_handler = CategoryHandler(home)

        year_month = self.request.GET.get("year_month", default_year_month())
        receipt_handler = ReceiptHandler(home, year_month)
        receipts = receipt_handler.get_queryset()

        purchase_item_handler = PurchaseItemHandler(receipts)

        context["shops"] = shop_handler.as_list()
        context["categories"] = category_handler.as_list()
        context["receipts"] = receipt_handler.as_list()
        context["purchase_items"] = purchase_item_handler.as_list()
        return context
