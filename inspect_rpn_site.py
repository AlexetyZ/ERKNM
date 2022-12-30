from main_ERKNM import erknm
from direct_pxl import Operation


class Inspect_site_information:
    def __init__(self):
        self.session = erknm(headless=False)
        pass

    def by_xl_file(self, path):
        o = Operation(path)
        ogrn_list = o.get_column_values('H')

        self.session.go_to_rpn_inspect_next_year()
        for number, ogrn in enumerate(ogrn_list):
            self.session.get_xl_list_ogrn_for_rpn_inspect(ogrn)
            command = input('Нажмите для продолжения:  q- пометить желтым')
            if command == 'q' or command == 'й':
                o.mark_cell(row=number+1, column=8, saving=False)

        o.save_document()



if __name__ == '__main__':
    Inspect_site_information().by_xl_file(
        "C:\\Users\\zaitsev_ad\Documents\ЕРКНМ\проверка состояния проверок на сайте\Республика Коми.xlsx"
    )