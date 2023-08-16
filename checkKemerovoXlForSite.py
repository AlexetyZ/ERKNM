import openpyxl
import os


class C:
    def __init__(self, path):
        self.wb = openpyxl.load_workbook(path)
        self.sh = self.wb.worksheets[0]

    def main(self):
        for row in self.sh.iter_rows(min_row=2, values_only=True):
            self.checkRow(row)
            break

    def checkRow(self, row):
        algorithm = {
            1: None
        }
        for n, consist in algorithm.items():
            if row[n] is algorithm[n]:
                print('совпало')




if __name__ == '__main__':
    C("C:\\Users\zaitsev_ad\Downloads\Сопоставление испр Кемерово_19.07.2023________.xlsx").main()
