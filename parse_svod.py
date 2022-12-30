from direct_pxl import Operation
import json
import os


class Svod:
    def __init__(self, svod_path, report_path):
        self.svod = Operation(svod_path)
        self.report = Operation(report_path)

    def main(self):
        sh_svod = self.svod.wb.worksheets
        for sheet in sh_svod:
            self.svod.sh = sheet
            try:
                region = self.svod.get_cell_value(row=3, column=4)
                for number, cell in enumerate(self.report.get_column_values('A')):
                    if cell == region:
                        self.report.change_value_in_cell(row=number+1, column=5, value=self.svod.get_cell_value(row=317, column=17))
            except:
                pass

        pass

class Gos_zadanie:
    def __init__(self, path):
        self.gz_year = Operation(path)


    def main(self, year):
        if not os.path.exists('fbuz_goszad_list.json'):

            fbuz_list = []
            names = self.gz_year.get_column_values('E')
            organization = {}
            last_inn = 0
            for number, name in enumerate(names):
                if number < 1:
                    continue
                row = number+1
                kbk = self.gz_year.get_cell_value(row=row, column=2)
                if not kbk:
                    if organization:
                        fbuz_list.append(organization)
                        organization = {}
                        # print(name)
                    if 'ЗДРАВООХРАНЕН' in name:
                        # print(name)
                        last_inn = self.gz_year.get_cell_value(row=row, column=3)
                        organization[last_inn] = {'org_name': name, 'services': {}}
                        continue
                else:
                    inn = self.gz_year.get_cell_value(row=row, column=3)
                    # print(inn, last_inn)
                    if inn == last_inn:
                        # print('инн совпало')
                        service_number = self.gz_year.get_cell_value(row=row, column=7)
                        service_indicator = self.gz_year.get_cell_value(row=row, column=8)
                        service_volume = self.gz_year.get_cell_value(row=row, column=10)
                        service_id = f'{name} ({service_indicator}) {service_number}'
                        if service_number:

                            if service_id in [serv for serv in list(organization[last_inn]['services'].keys())]:
                                previous_service_volume = organization[last_inn]['services'][service_id]['service_volume'][year]
                                organization[last_inn]['services'][service_id]['service_volume'][year] = service_volume + previous_service_volume
                            else:
                                organization[last_inn]['services'][service_id] = {'service_number': service_number}
                                organization[last_inn]['services'][service_id]['service_name'] = name


                                organization[last_inn]['services'][service_id]['service_indicator'] = service_indicator


                                # try:
                                    # print(organization[last_inn]['services'][service_id])
                                # except:
                                #     pass
                                organization[last_inn]['services'][service_id]['service_volume'] = {year: 0}
                                organization[last_inn]['services'][service_id]['service_volume'][year] = service_volume
            with open('fbuz_goszad_list.json', 'w') as file:
                json.dump(fbuz_list, file)
        # print(fbuz_list)
        else:
            with open('fbuz_goszad_list.json', 'r') as file:
                fbuz_list = json.load(file)
            print('уже есть файл')
            organization = {}
            last_inn = 0
            old_organization = ''

            # current_inn = '3017042340'
            # if current_inn in [list(org.keys())[0] for org in fbuz_list]:
            #     print('есть организация')



            names = self.gz_year.get_column_values('E')
            for number, name in enumerate(names):
                if number < 1:
                    continue
                row = number + 1
                kbk = self.gz_year.get_cell_value(row=row, column=2)
                if not kbk:
                    if organization:

                        try:
                            fbuz_list.remove([obj for obj in fbuz_list if last_inn == list(obj.keys())[0]][0])
                        except:
                            print(old_organization, last_inn)
                            raise ValueError('NO')
                        fbuz_list.append(organization)
                        organization = {}
                    if 'ЗДРАВООХРАНЕН' in name:
                        current_inn = str(self.gz_year.get_cell_value(row=row, column=3))
                        if current_inn in [list(org.keys())[0] for org in fbuz_list]:
                            # print('есть организация')
                            organization = [org for org in fbuz_list if list(org.keys())[0] == current_inn][0]
                            old_organization = organization
                            last_inn = current_inn
                        else:
                            organization[current_inn] = {'org_name': name, 'services': {}}
                            last_inn = current_inn


                        continue
                else:

                    inn = self.gz_year.get_cell_value(row=row, column=3)
                    print(inn, last_inn)
                    if str(inn) == str(last_inn):
                        print('смовпадает')
                        service_number = self.gz_year.get_cell_value(row=row, column=7)
                        service_indicator = self.gz_year.get_cell_value(row=row, column=8)
                        service_volume = self.gz_year.get_cell_value(row=row, column=10)
                        service_id = f'{name} ({service_indicator}) {service_number}'
                        if service_number:
                            print(str(last_inn), [list(org.keys())[0] for org in fbuz_list])
                            if str(last_inn) in [list(org.keys())[0] for org in fbuz_list]:

                                organization = [org for org in fbuz_list if list(org.keys())[0] == last_inn][0]
                                services = organization[last_inn]['services']
                                # fbuz_list.pop(fbuz_list.index(organization))
                                print(services)
                                if service_id in [serv for serv in list(organization[last_inn]['services'].keys())]:
                                    print('услуга есть')



                                    if not year in list(organization[last_inn]['services'][service_id]['service_volume'].keys()):
                                        organization[last_inn]['services'][service_id]['service_volume'][year] = service_volume

                                    else:
                                        previous_service_volume = organization[last_inn]['services'][service_id]['service_volume'][year]
                                        organization[last_inn]['services'][service_id]['service_volume'][year] = service_volume + previous_service_volume

                                else:
                                    print("услуги нет")
                                    print(service_id)
                                    organization[last_inn]['services'][service_id] = {'service_number': service_number}
                                    organization[last_inn]['services'][service_id]['service_name'] = name
                                    organization[last_inn]['services'][service_id]['service_indicator'] = service_indicator
                                    organization[last_inn]['services'][service_id]['service_volume'] = {year: 0}
                                    organization[last_inn]['services'][service_id]['service_volume'][year] = service_volume
                        # print(organization)
                    else:
                        print('не совпало')
            with open('fbuz_goszad_list.json', 'w') as file:
                json.dump(fbuz_list, file)



            # year = '2023'
            # service_volume = 10000.0
            # service_number = '869000Ф.99.1.АЕ12АА01000'
            # name = 'новый Учет инфекционных заболеваний, профессиональных заболеваний, массовых неинфекционных заболеваний (отравлений) в связи с вредным воздействием факторов среды обитания человека'
            # service_indicator = 'Количество заполненных карт учета заболевших лиц (актов расследования)'
            # service_id = f'{name}{service_number}{service_indicator}'
            #
            # last_inn = '3017042340'



class Create_report:
    def __init__(self):
        with open('fbuz_goszad_list.json', 'r') as file:
            self.fbuz_list = json.load(file)


    def main(self):
        o = Operation()
        o.change_value_in_cell(row=3, column=2, value='Краткое название учреждения', saving=False)

        for number, fbuz in enumerate(self.fbuz_list):


            org_inn = list(fbuz.keys())[0]
            organization = list(fbuz.values())[0]
            org_name = organization['org_name']



            services = organization['services']

            # print(services)
            last_row = o.detect_last_row()
            current_row = 0
            for row in range(3, last_row):
                if o.get_cell_value(row=2, column=row) == org_inn:
                    current_row = row
            if current_row == 0:
                current_row = last_row
                o.change_value_in_cell(row=current_row, column=2, value=org_name, saving=False)
                o.change_value_in_cell(row=current_row, column=1, value=org_inn, saving=False)

            for service_id, service_detail in services.items():
                service_volume = service_detail['service_volume']
                service_name = service_detail['service_name']
                service_indicator = service_detail['service_indicator']
                service_number = service_detail['service_number']
                last_column = o.detect_last_column()
                current_first_column = 0
                for column in range(3, last_column):
                    if o.get_cell_value(row=1, column=column) == service_id:
                        current_first_column = column
                if current_first_column == 0:
                    current_first_column = last_column
                    o.change_value_in_cell(row=3, column=current_first_column, value=2022, saving=False)
                    o.change_value_in_cell(row=3, column=current_first_column+1, value=2023, saving=False)
                    o.change_value_in_cell(row=2, column=current_first_column, value=service_number, saving=False)
                    o.change_value_in_cell(row=2, column=current_first_column+1, value=" ", saving=False)
                    o.change_value_in_cell(row=1, column=current_first_column, value=service_id, saving=False)
                    o.change_value_in_cell(row=1, column=current_first_column+1, value=" ", saving=False)




                try:
                    o.change_value_in_cell(row=current_row, column=current_first_column, value=service_volume['2022'], saving=False)
                except:
                    o.change_value_in_cell(row=current_row, column=current_first_column, value=None, saving=False)
                try:
                    o.change_value_in_cell(row=current_row, column=current_first_column + 1, value=service_volume['2023'], saving=False)
                except:
                    o.change_value_in_cell(row=current_row, column=current_first_column + 1, value=None, saving=False)

                o.save_document(path="C:\\Users\zaitsev_ad\Desktop\ОБАС")










if __name__ == '__main__':
    # svod = Svod(
    #     svod_path="C:\\Users\zaitsev_ad\Documents\ЕРКНМ\Проверка свода\СВОД РФ_Ежегодный план КНМ на 2023 год___на 16.12.2022.xlsx",
    #     report_path="C:\\Users\zaitsev_ad\Documents\ЕРКНМ\Проверка свода\\report_objects 2022-12-21.xlsx"
    # )
    # svod.main()

    # gz = Gos_zadanie("C:\\Users\zaitsev_ad\Desktop\ГЗ 2022-2023\ГЗ 2023.xlsx")
    # gz.main(year=2023)
    if os.path.exists("C:\\Users\zaitsev_ad\Desktop\ОБАС.xlsx"):
        report = Create_report()
        report.main()
    else:
        report = Create_report()
        report.main()
