from main_ERKNM import erknm
import openpyxl
from data_description import rename_tu_dict

class Table_erknm:
    def __init__(self, wb_path_1):
        self.wb_path_1 = wb_path_1
        self.wb_1 = openpyxl.load_workbook(self.wb_path_1)

    def rename_tu(self):
        sh = self.wb_1.worksheets[5]
        for n, row in enumerate(sh.iter_rows(min_row=4, values_only=True)):
            new_tu_name = rename_tu_dict[row[0]]
            sh.cell(column=1, row=n+4, value=new_tu_name)
        self.wb_1.save(self.wb_path_1)

    def main(self):
        pass

    def create_dict(self):
        """

        @return:
        """
        tu_dict = {}
        sh = self.wb_1.worksheets[0]
        for row in sh.iter_rows(min_row=2, values_only=True):
            tu_dict[row[4]] = row[2]
        return tu_dict


if __name__ == '__main__':
    path = "C:\\Users\zaitsev_ad\Documents\ЕРКНМ\отчеты ГАСУ\\2022.xlsx"
    Table_erknm(path).rename_tu()
