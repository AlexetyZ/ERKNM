from exp import simple_analys_from_db, request_db
from sql import Database


d = Database()


def simple_analys():
    simple_analys_from_db(
        targets=['controll_organ'],
        year=2022,
        status=[
            'Завершено',
            # 'Решение обжаловано',
            # 'В процессе заполнения',
            # 'Ожидает завершения',
            # 'Не может быть проведено',
            # 'Не согласована',
            # 'Исключена'
        ],
        stop_date=[
            '2022-01-01', '2022-03-31'
            # '2022-04-01', '2022-06-30'
            # '2022-07-01', '2022-09-30'

        ],
        # stop_date='1900-01-01',
        type=[
            'Внеплановое КНМ',
            # 'Плановое КНМ',
            # 'Плановая проверка по 248-ФЗ (утвержденная по плану 294-ФЗ)'
        ],
        controll_organ=[
            'Управление Роспотребнадзора по Республике Бурятия',
            'Управление Роспотребнадзора по Республике Саха (Якутия)',
            'Управление Роспотребнадзора по Забайкальскому краю',
            'Управление Роспотребнадзора по Камчатскому краю',
            'Управление Роспотребнадзора по Приморскому краю',
            'Управление Роспотребнадзора по Хабаровскому краю',
            'Управление Роспотребнадзора по Амурскоу области',
            'Управление Роспотребнадзора по Магаданской области',
            'Управление Роспотребнадзора по Сахалинской области',
            'Управление Роспотребнадзора по о Еврейской автономной области',
            'Управление Роспотребнадзора по Чукотскому автономному округу'
        ]

    )


def get_knm_with_no_stop_date():
    """
    Ищет проверки, у которых нету даты окончания среди завершенных (за определенный период) и выдает из номера
    @return:
    """
    text_request = request_db(
        targets=['id'],
        year=2022,
        status=[
            'Завершено',
            # 'Решение обжаловано',
            # 'В процессе заполнения',
            # 'Ожидает завершения',
            # 'Не может быть проведено',
            # 'Не согласована',
            # 'Исключена'
        ],
        start_date=['2022-01-01', '2022-09-30'],
        stop_date='1900-01-01',
        controll_organ=[
            'Управление Роспотребнадзора по Республике Бурятия',
            'Управление Роспотребнадзора по Республике Саха (Якутия)',
            'Управление Роспотребнадзора по Забайкальскому краю',
            'Управление Роспотребнадзора по Камчатскому краю',
            'Управление Роспотребнадзора по Приморскому краю',
            'Управление Роспотребнадзора по Хабаровскому краю',
            'Управление Роспотребнадзора по Амурскоу области',
            'Управление Роспотребнадзора по Магаданской области',
            'Управление Роспотребнадзора по Сахалинской области',
            'Управление Роспотребнадзора по о Еврейской автономной области',
            'Управление Роспотребнадзора по Чукотскому автономному округу'
        ]
    )

    result = Database().take_request_from_database(text_request)
    return result


def get_true_stop_date_if_not(s, erknm_id):
    """
    Используется для мультипроцессинга

    @param s: сессия в еркнм
    @param d: сессия в базе данных
    @param erknm_id:
    @return:
    """
    erpId = erknm_id[0]
    full_knm_info = s.get_knm_by_number(erpId)
    true_stop_date = full_knm_info['knmErknm']['organizations'][0]['act']['nextWordDayActDateTime']
    d.change_stop_date_by_erpID(true_stop_date, erpId)
    print('сделано')


if __name__ == '__main__':
    result = simple_analys()

    print(result)
