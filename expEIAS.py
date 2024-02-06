import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.807 YaBrowser/23.11.1.807 (corp) Yowser/2.5 Safari/537.36',
}
cookies = {
            'last_login_u_id': '957306',
            '_ym_uid': '1705405856636899637',
            '_ym_d': '1705405856',
            '_clck': 'gd5iim%7C2%7Cfig%7C0%7C1476',
            '_ga_GYKLT1ZMTB': 'GS1.1.1705405928.1.1.1705405936.0.0.0',
            'xcuser_sess': '7198b486-bac1-11ee-ab55-003048bddde7',
            'xcuser_action': '3de425d8-bac5-11ee-ab55-003048bddde7',
            'metabase.DEVICE': '9d4841f3-ef7f-4c99-bba5-b67a0e827610',
            '_ga': 'GA1.2.1617587542.1705405929',
            '_gid': 'GA1.2.364273186.1707148477',
            'employee_guid': '95c50716%2Da840%2D11ed%2D8444%2D005056958e11',
            'name': '%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B9',
            'patronymic': '%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B5%D0%B2%D0%B8%D1%87',
            'regions': '1%7C4%7C22%7C28%7C30%7C29%7C99%7C2%7C31%7C32%7C3%7C33%7C34%7C35%7C36%7C5%7C93%7C79%7C90%7C75%7C37%7C6%7C38%7C7%7C39%7C8%7C40%7C41%7C9%7C10%7C42%7C43%7C11%7C44%7C23%7C24%7C91%7C45%7C46%7C47%7C48%7C94%7C49%7C12%7C13%7C77%7C50%7C51%7C52%7C83%7C53%7C54%7C55%7C56%7C57%7C58%7C59%7C25%7C60%7C61%7C62%7C63%7C78%7C64%7C65%7C14%7C66%7C92%7C15%7C26%7C67%7C68%7C69%7C16%7C70%7C71%7C17%7C18%7C72%7C73%7C27%7C19%7C86%7C95%7C74%7C20%7C21%7C87%7C89%7C76%7C100%7C101%7C102%7C103%7C104%7C105%7C106%7C107',
            'surname': '%D0%97%D0%B0%D0%B9%D1%86%D0%B5%D0%B2',
            'user_id': 'c24e3f41%2D7f46%2D4e3e%2D8ade%2Dd1c8de06eecf',
            'roles': 'gov%2Dservices%5Fui%2Cgu%5Fspecialist%5Felmk%2Cknd%5Ffederal%5Fspecialist%2Crhs%5Ffederal%5Fspecialist%2Crhs%5Fui%2Crole%5Fuser%5Ffcgie',
            'employee': '95c50716%2Da840%2D11ed%2D8444%2D005056958e11',
            'position': '%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D0%BD%D0%B8%D0%BA',
            'email': 'zaitsev%5Fad%40rospotrebnadzor%2Eru',
            'SESSION_master': 'IjI0MjE3ZTZhLTc4MDAtNGFmMi1hZjg1LTE3MDU3ZWRiMDdmMSI%3D%2EHaY7xgdHkwi21PIwxCh5kHI7Ix3Gw1bDKhypYQUxnfg%3D',
        }
response = requests.get(
    'https://eias.rospotrebnadzor.ru/api/households/industrial_objects/v2?limit=50&sort=created_at&region=in::1&has_liquidated_date=false&supervised_status=in::supervised',
    headers=headers,
    cookies=cookies
)
print(response.json())
