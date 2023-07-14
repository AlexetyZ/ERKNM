

def main(sov_date, sov_time, patron, other_participant, all_participants, sov_theme, decision):
    message = 'Проведено совещание '
    message += f'{sov_date} в '
    message += f'{sov_time} '
    message += f'{patron}'
    if other_participant:
        message += f', совместно с представителями {other_participant}. '
    else:
        message += '. '

    message += f'Участники совещания: {all_participants}. '
    message += f'Тема совещания: "{sov_theme}". '
    message += f'По итогу {decision}'

    return message


if __name__ == '__main__':
    sov_date = input('дата')
    sov_time = input('время')
    patron = input('кем проводилось совещание?(ex: Роспотребнадзором)')
    other_participant = input('кто был из других организаций(ex: совместно с представителями ....)')
    all_participants = input('полный перечень участников (ex: Управление Роспотребнадзора по ...)')
    sov_theme = input('Тема совещания (ex: Разработка функционала)')
    decision = input('принято решение, озвучена позиция (ex: принято решение разработать функционал)')

    print(main(sov_date, sov_time, patron, other_participant, all_participants, sov_theme, decision))
