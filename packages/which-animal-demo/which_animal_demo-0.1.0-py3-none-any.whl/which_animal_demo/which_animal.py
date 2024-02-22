import argparse
from datetime import datetime

from lunardate import LunarDate

LUNAR_ZODIAC = {
    0: 'Monkey',
    1: 'Rooster',
    2: 'Dog',
    3: 'Pig',
    4: 'Rat',
    5: 'Ox',
    6: 'Tiger',
    7: 'Rabit',
    8: 'Dragon',
    9: 'Snake',
    10: 'Horse',
    11: 'Sheep',
}


def animal_of_year(year: int) -> str:
    return LUNAR_ZODIAC[year % 12]


def animal_of_date(year: int, month: int, day: int) -> str:
    year = LunarDate.fromSolarDate(
        year=year,
        month=month,
        day=day,
    ).year
    return animal_of_year(year)


def convert_str_to_dtime(date_str: str) -> datetime:
    date_format = '%Y-%m-%d'
    return datetime.strptime(date_str, date_format)


def main():
    parser = argparse.ArgumentParser(
        prog='which-animal',
        description='Given a date, tell you which animal of lunar zodiac it belongs to',
        epilog='Text at the bottom of help',
    )
    parser.add_argument('date')
    args = parser.parse_args()
    date_obj = convert_str_to_dtime(args.date)
    print(animal_of_date(
        year=date_obj.year,
        month=date_obj.month,
        day=date_obj.day,
    ))


if __name__ == '__main__':
    main()
