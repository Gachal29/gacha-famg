import uuid
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db import models

from .util import generate_hid, default_year_month, defualt_year_month_start_date
from .validate import validate_year_month_format


app_name = "db"

class Home(models.Model):
    class Meta:
        db_table = "homes"
        verbose_name = verbose_name_plural = "ホーム"

    hid = models.CharField(
        verbose_name="Home ID",
        max_length=10,
        unique=True,
        default=generate_hid,
        editable=False,
    )
    name = models.CharField(
        verbose_name="名前",
        max_length=150
    )
    users = models.ManyToManyField(
        User,
        through=f"{app_name}.HomeUser"
    )

    def __str__(self):
        return f"{self.pk}: {self.name}"
    

class HomeUser(models.Model):
    class Meta:
        db_table = "home_users"
        verbose_name = verbose_name_plural = "ホームに所属するユーザー"
        constraints = [
            models.UniqueConstraint(
                fields=["home", "user"],
                name="unique_home_user"
            )
        ]

    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.home}, {self.user}"
    

class Category(models.Model):
    class Meta:
        db_table = "categories"
        verbose_name = verbose_name_plural = "カテゴリー"
        constraints = [
            models.UniqueConstraint(
                fields=["home", "name"],
                name="unique_home_category_name"
            )
        ]

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="カテゴリ名",
        max_length=150,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="表示優先度",
        default=0,
        validators=[MaxValueValidator(32767)]
    )

    def __str__(self):
        return f"{self.home}, {self.name}"
    

class Shop(models.Model):
    class Meta:
        db_table = "shops"
        verbose_name = verbose_name_plural = "ショップ"
        constraints = [
            models.UniqueConstraint(
                fields=["home", "name"],
                name="unique_home_shop"
            )
        ]

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name="ショップ名",
        max_length=150,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="表示優先度",
        default=0,
        validators=[MaxValueValidator(32767)]
    )
    text_color = models.CharField(
        verbose_name="テキストカラー",
        max_length=7,
        default="#0D0D0D"
    )
    bg_color = models.CharField(
        verbose_name="背景カラー",
        max_length=7,
        default="#DAD5D2"
    )

    def __str__(self):
        return f"{self.home}, {self.name}"
    

class PurchaseRecordMonth(models.Model):
    class Meta:
        db_table = "purchase_record_months"
        verbose_name = verbose_name_plural = "購入記録の月管理"

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
    )
    year_month = models.CharField(
        verbose_name="年月",
        max_length=7,
        default=default_year_month,
        validators=[validate_year_month_format]
    )
    date = models.DateField(
        verbose_name="月初の日付",
        default=defualt_year_month_start_date,
    )

    def __str__(self):
        return f"{self.home}, {self.year_month}"
    

class Receipt(models.Model):
    class Meta:
        db_table = "receipts"
        verbose_name = verbose_name_plural = "レシート"
    
    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name="日付",
        default=timezone.now,
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}: {self.home.name}, {self.date}"
    

class PurchaseItem(models.Model):
    class Meta:
        db_table = "purchase_items"
        verbose_name = verbose_name_plural = "購入品記録"
    
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    detail = models.TextField(verbose_name="詳細")
    price = models.IntegerField(verbose_name="金額", validators=[MinValueValidator(0)])
    discount = models.IntegerField(
        verbose_name="割引額",
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    note = models.TextField(
        verbose_name="備考",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.receipt.id}: {self.receipt.home.name}, {self.category.name}"
