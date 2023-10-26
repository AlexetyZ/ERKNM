import openpyxl
from Dictionary import tuRegExp
import re
from tqdm import tqdm
from datetime import datetime


def main(path):

    wb = openpyxl.load_workbook(path)
    sh = wb.worksheets[0]
    for row in tqdm(sh.iter_rows(min_row=2, max_col=3)):
        for reg, val in tuRegExp.items():
            if re.search(reg, str(row[0].value).lower()):
                row[1].value = val
                break
    wb.save(path)


if __name__ == '__main__':
    path = "C:\\Users\zaitsev_ad\Desktop\регионы.xlsx"
    main(path)
