import openpyxl


def merge(ervk: str, plan: str):
    wb_ervk = openpyxl.load_workbook(ervk)
    wb_plan = openpyxl.load_workbook(plan)
    sh_ervk = wb_ervk.worksheets[0]
    sh_plan = wb_plan.worksheets[0]
    plan_ogrns = [cell.value for cell in sh_plan['I'] if cell.value]
    for n, ervk_cell in enumerate(sh_ervk['W']):
        if ervk_cell.value in plan_ogrns:
            sh_ervk[f'Y{n+1}'].value = 'есть в плане'

    wb_ervk.save(ervk)


if __name__ == '__main__':
    ervk = "S:\\Зайцев_АД\Выверка ЕРВК\заносить вручную\Добавление в ЕРВК (2) — копия.xlsx"
    plan = "C:\\Users\zaitsev_ad\Downloads\\2023050127_утвержденный_план (1).xlsx"
    merge(ervk, plan)

