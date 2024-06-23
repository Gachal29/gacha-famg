import { Shop, Category, Receipt } from "../model/finance-model";

export class FinanceController {
  shops: Array<Shop>
  categories: Array<Category>
  receipts: Array<Receipt>
  innerWidth: number

  constructor(
    shops: Array<any>, categories: Array<any>, receipts: Array<any>, purchase_items: Array<any>, innerWidth: number
  ) {
    this.shops = shops.map((shop) => Shop.fromData(shop));
    this.categories = categories.map((category) => Category.fromData(category));
    this.receipts = receipts.map((receipt) => {
      const data = JSON.parse(JSON.stringify(receipt));
      data.purchase_items = purchase_items.filter((purchaseItem) => receipt.id === purchaseItem.receipt_id);
      return Receipt.fromData(data);
    });
    this.innerWidth = innerWidth;
  }

  getShop(shopId: number | null): Shop | undefined {
    return this.shops.find((shop) => shop.id === shopId);
  }

  getCategory(categoryId: number | null): Category | undefined {
    return this.categories.find((category) => category.id === categoryId);
  }
}
