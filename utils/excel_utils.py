""" Утилиты для работы с MS Excel"""
import datetime
import typing
from dataclasses import dataclass

import pandas as pd


@dataclass
class ScheduleItem:
    """
    Класс для проверки сохранения расписания
    """
    resource_id: int
    task_id: int
    start_time: int
    end_time: int
    cost: float


def save_schedule_to_excel(schedule, filename: str):
    """
    Сохраняет расписание в файл, добавляя к началу названия файла текущее время
    :param schedule:
    :param filename:
    :return:
    """
    filename = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + "_" + filename

    schedule_df = pd.DataFrame(schedule)
    schedule_df.to_excel(filename)


def get_excel_data(filename: str, sheet_name: str) -> list:
    """
    Возвращает данные из Excel-файла
    :param filename:
    :param sheet_name:
    :return:
    """
    df = pd.read_excel(filename, sheet_name=sheet_name)
    df_index = df.to_dict('index')
    resulted_list = list(df_index.values())
    return resulted_list


if __name__ == "__main__":
    result = get_excel_data('../Исходные данные.xlsx', 'Курьеры')
    for rec in result:
        print(rec)
    # test_schedule = [ScheduleItem(1, 2, 3, 4, 5), ScheduleItem(1, 3, 6, 7, 9)]
    # save_schedule_to_excel(test_schedule, "res.xlsx")
