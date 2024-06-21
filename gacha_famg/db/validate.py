from django.core.exceptions import ValidationError


def validate_year_month_format(value):
    ERROR_MSG = "年月は'YYYY_MM'の形式で入力してください。"
    split = value.split("_")
    if len(split) != 2:
        raise ValidationError(ERROR_MSG, params={"value": value})
    if len(split[0]) != 4 or len(split[1]) != 2:
        raise ValidationError(ERROR_MSG, params={"value": value})
    