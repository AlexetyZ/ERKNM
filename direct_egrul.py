import random
import time

from EGRUL import Egrul
import openpyxl


class Direct:

    def __init__(self):
        main_menu = input(
            'Выберите действие:\n 1. быстро найти организацию в егрюл\n 2. найти сведения об организациях по ИНН в файле XLSX\n')
        if main_menu == '1':
            org_info = self.get_org_info()
            self.find_info(org_info)
        if main_menu == '2':
            path = self.get_exelfile_path()
            inn_letter = input('Введите букву столбца, содержащий ИНН (большую латинскую)')
            ogrn_letter = input('Введите букву столбца, куда следует вставлять ОГРН (большую латинскую)')
            self.get_values_from_table(path, inn_letter, ogrn_letter)

    def get_exelfile_path(self):
        print(
            'Абсолютный путь до файла - путь начитая с расположения на диске/папке/и тд. Его можно получить через буфер обмена методом "Скопировать путь"')
        print("ВАЖНО!!!")
        print()
        print(
            'Для корректной работы, введите столбец, откуда будем брать ИНН, а так же, столбец, куда будем вставлять ОРГН. Начало перебора ИНН из таблицы начнется со строки 2. Убедитесь, что файл не открыт и сохранен в корректном формате')
        print()
        print("ВАЖНО!!!")
        paths = input('ВВЕДИТЕ АБСОЛЮТНЫЙ ПУТЬ ДО ОБРАБАТЫВАЕМОГО ФАЙЛА')
        path = paths.replace(paths[:1], '').replace(paths[:-1], '')
        return path

    def get_values_from_table(self, path, inn_letter, ogrn_letter):
        wb = openpyxl.load_workbook(path)
        sh = wb.active
        inn_table = sh[f'{inn_letter}']
        ogrn_table = sh[f'{ogrn_letter}']
        for inn_cell in inn_table:
            if inn_cell.row > 1:
                if inn_cell.value is None:
                    print('Пустой ИНН')
                    continue
                if sh.cell(inn_cell.row, column=ogrn_table[0].column).value is not None:
                    print('Уже заполнено огрн')
                    continue

                # print(inn_cell.value)

                result = self.find_info(inn_cell.value)



                sh.cell(row=inn_cell.row, column=ogrn_table[0].column, value=result)
                wb.save(path)
                time.sleep(1)

    def get_org_info(self):
        org_info = input('введите известную информацию об учреждении')
        return org_info

    def find_info(self, org_info):
        find_in_egrul = Egrul().find_in_egrul

        result = find_in_egrul(org_info)['o']
        print(result)
        return result


if __name__ == '__main__':
    Direct()
