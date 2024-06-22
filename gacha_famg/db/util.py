import datetime
import random, string
from .validate import validate_year_month_format


def generate_hid():
    # hidを生成する
    HID_LENGTH = 10
    AVAILABLE_LETTERS = string.ascii_letters + string.digits

    rand_letters = [random.choice(AVAILABLE_LETTERS) for i in range(HID_LENGTH)]
    return "".join(rand_letters)

def default_year_month():
    today = datetime.date.today()
    year = today.year
    month = today.month
    if month < 10:
        month = f"0{month}"
    return f"{year}_{month}"

def defualt_year_month_start_date():
    # 前月の25日から月をスタートする
    DEFAULT_START_DAY = "25"
    year_month = default_year_month()
    year_month_split = year_month.split("_")
    month = int(year_month_split[1])-1
    if month == 0:
        month = 12
    if month < 10:
        month = f"0{month}"
    date = datetime.datetime.strptime(f"{year_month_split[0]}_{month}_{DEFAULT_START_DAY}", "%Y_%m_%d").date()
    return date

def get_next_year_month(year_month):
    validate_year_month_format(year_month)
    year_month_split = year_month.split("_")
    year = int(year_month_split[0])
    month = int(year_month_split[1])
    month += 1
    if month == 13:
        month = 1
        year += 1
    if month < 10:
        month = f"0{month}"
    return f"{year}_{month}"
