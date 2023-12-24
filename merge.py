from Dictionary import tuRegExp
import openpyxl
import re


def main(path, tuCurCol, tuNeedCol):
    wb = openpyxl.load_workbook(path)
    sh = wb.worksheets[0]
    for row in sh.iter_rows(min_row=1, max_col=tuNeedCol+1):
        tuCur = row[tuCurCol].value
        for reg, trTu in tuRegExp.items():
            if re.search(reg, str(tuCur).lower()):
                row[tuNeedCol].value = trTu
    wb.save(path)


if __name__ == '__main__':
    path = '/Users/aleksejzajcev/Downloads/Плановые_проверки_2018_2023_планом_на_2024_г_итог_динамика (1).xlsx'
    main(
        path='/Users/aleksejzajcev/Downloads/О_запланированных_на_2024_год_профилактических_визитах_17_10_2023.xlsx',
        tuCurCol=0,
        tuNeedCol=3
    )