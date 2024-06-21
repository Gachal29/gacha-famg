from django.db import models

from db.models import Home
from db.util import default_year_month, defualt_year_month_start_date
from db.validate import validate_year_month_format


class ImportPurchaseRecordFile(models.Model):
    class Meta:
        managed = False
        verbose_name = verbose_name_plural = "家計簿ファイルインポート"

    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE
    )
    year_month = models.CharField(
        verbose_name="年月",
        max_length=7,
        default=default_year_month,
        validators=[validate_year_month_format],
    )
    date = models.DateField(
        verbose_name="月初めの日付",
        default=defualt_year_month_start_date,
    )
    file = models.FileField("インポートするファイル（Excel）")

    def __str__(self):
        return f"{self.file.name}"