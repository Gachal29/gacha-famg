

export class Shop {
  id: number
  name: string
  textColor: string | null
  bgColor: string | null

  constructor(id: number, name: string, text_color: string | undefined, bg_color: string | undefined) {
    this.id = id
    this.name = name
    this.textColor = text_color ?? null
    this.bgColor = bg_color ?? null
  }

  static fromData(data: any): Shop {
    return new Shop(
      data.id,
      data.name,
      data.text_color,
      data.bg_color,
    )
  }

  get badgeStyle() {
    return {
      color: this.textColor ?? "",
      background: this.bgColor ?? "",
      borderWidth: 0,
    }
  }
}

export class Category {
  id: number
  name: string
  textColor: string | null
  bgColor: string | null

  constructor(id: number, name: string, text_color: string | undefined, bg_color: string | undefined) {
    this.id = id
    this.name = name
    this.textColor = text_color ?? null
    this.bgColor = bg_color ?? null
  }

  static fromData(data: any): Category {
    return new Category(
      data.id,
      data.name,
      data.text_color,
      data.bg_color,
    )
  }

  get badgeStyle() {
    return {
      color: this.textColor ?? "",
      background: this.bgColor ?? "",
      borderWidth: 0,
    }
  }
}

export class PurchaseItem {
  id: number
  receiptId: string
  categoryId: number | null
  detail: string
  price: number
  discount: number | null
  note: string | null

  constructor(
    id: number,
    receipt_id: string,
    category_id: number | undefined,
    detail: string,
    price: number,
    discount: number | undefined,
    note: string | undefined
  ) {
    this.id = id
    this.receiptId = receipt_id
    this.categoryId = category_id ?? null
    this.detail = detail
    this.price = price
    this.discount = discount ?? null
    this.note = note ?? null
  }

  static fromData(data: any) {
    return new PurchaseItem(
      data.id,
      data.receipt_id,
      data.category_id,
      data.detail,
      data.price,
      data.discount,
      data.note,
    )
  }

  get priceTitle() {
    if (this.discount) {
      return `${(this.price - this.discount).toLocaleString()}円`;
    }
    return `${this.price.toLocaleString()}円`;
  }
}

export class Receipt {
  id: string
  date: Date
  shopId: number | null
  purchaseItems: Array<PurchaseItem>

  constructor(
    id: string,
    date: string,
    shop_id: number | undefined,
    purchase_items: Array<any> | undefined
  ) {
    this.id = id
    this.date = new Date(date)
    this.shopId = shop_id ?? null
    this.purchaseItems = purchase_items?.map((purchaseItem) => PurchaseItem.fromData(purchaseItem)) ?? [];
  }

  static fromData(data: any) {
    return new Receipt(
      data.id,
      data.date,
      data.shop_id,
      data.purchase_items,
    )
  }

  get totalPrice(): string {
    let totalPrice = 0;
    this.purchaseItems.forEach((item) => {
      totalPrice += item.price;
      if (item.discount) {
        totalPrice -= item.discount;
      }
    });
    return `${totalPrice.toLocaleString()}円`;
  }
}
