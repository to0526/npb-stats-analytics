from datetime import datetime

def calc_age(birth_year: int, target_year: int | None = None) -> int:
    if target_year is None:
        target_year = datetime.now().year
    return target_year - birth_year

def age_category(age: int) -> str:
    if age <= 24:
        return "若手"
    elif age <= 32:
        return "中堅"
    else:
        return "ベテラン"
