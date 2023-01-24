import openpyxl
import os
from sql import Database


ws = openpyxl.load_workbook("C:\\Users\zaitsev_ad\Desktop\Номера.xlsx")
sh = ws.worksheets[0]


def change_violation_submitted():
    numbers = set([cell.value for cell in sh['B']])
    Database().change_violation_submitted_in_inspections(numbers)


def main():
    change_violation_submitted()


if __name__ == '__main__':
    main()
