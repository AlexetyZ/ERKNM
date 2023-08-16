from datetime import datetime, timedelta

"""
exists - наличие показателя
dateLimit - дата, являющаяся границей актуальности показателя (ех: крайняя дата проведения исследования, являющаяся актуальной)
datetime.now() - текущая дата
study_programm - программа гигиенического обучения и аттестации
age - возраст (полных лет)
gender - пол ()
had_measles - болел ли корью?(да, нет)
had_rubella - болел ли краснухой(да, нет)
"""


class ELMKRequirements:
    def __init__(self, gender: str, age: int, had_measles: bool, had_rubella: bool):
        self.gender = gender
        self.age = age
        self.had_measles = had_measles
        self.had_rubella = had_rubella

    def workWithFoodWithoutCream(self):
        return {
            "Исследование крови на сифилис": {
                'exists': True,
                'dateLimit': datetime.now()-timedelta(days=365)
            },
            "Исследования на носительство возбудителей шигеллёза": {'exists': True, 'dateLimit': False},
            "Исследования на носительство возбудителей камбиобактериоза": {'exists': True, 'dateLimit': False},
            "Исследования на носительство возбудителей сальмонеллёза": {'exists': True, 'dateLimit': False},
            "Исследования на носительство норовируса": {'exists': True, 'dateLimit': False},
            "Исследования на носительство ротовируса": {'exists': True, 'dateLimit': False},
            "серологическое обследование на брюшной тиф": {'exists': True, 'dateLimit': False},
            "Исследования на гельминтозы": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Мазок из зева и носа на наличие патогенного стафилококка": {'exists': True, 'dateLimit': False},
            "Флюорография или рентгенография легких в двух проекциях (прямая и правая боковая)": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

            "Врач-оториноларинголог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Врач-дерматовенеролог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Врач-стоматолог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "врач-терапевт": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "врач-профпатолог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

            "Прививка столбняк/дифтерия": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365*10)},
            "Прививка RW I вирусный гепатит В": {'exists': True if 18 <= self.age < 55 else False, 'dateLimit': True},
            "Прививка RW II вирусный гепатит В": {'exists': True if 18 <= self.age < 55 else False, 'dateLimit': True},
            "Прививка RW III вирусный гепатит В": {'exists': True if 18 <= self.age < 55 else False, 'dateLimit': True},
            "Прививка I корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка II корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка I краснуха": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка II краснуха": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка грипп": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка ВГА": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка шигеллез": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Прививка SARS-CoV-2": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

            "Иммунный статус корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Иммунный статус дифтерия": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Иммунный статус столбняк": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
            "Иммунный статус гепатит": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

            "гигиеническое обучение": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365), "study_programm": "Работы, где имеется контакт с пищевыми продуктами в том числе с кремами и пр."},
            "гигиеническая аттестация": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365), "study_programm": "Работы, где имеется контакт с пищевыми продуктами в том числе с кремами и пр."},

        }





example = {
    "Исследование крови на сифилис": {'exists': True, 'dateLimit': datetime.now()-timedelta(days=365)},
    "Исследования на носительство возбудителей шигеллёза": {'exists': True, 'dateLimit': datetime.now()-timedelta(days=365)},
    "Исследования на носительство возбудителей камбиобактериоза": {'exists': True, 'dateLimit': datetime.now()-timedelta(days=365)},
    "Исследования на носительство возбудителей сальмонеллёза": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Исследования на носительство  норовируса": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Исследования на носительство ротовируса": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "серологическое обследование на брюшной тиф": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Исследования на гельминтозы": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Мазок из зева и носа на наличие патогенного стафилококка": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Мазки на гонорею ": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Флюорография или рентгенография легких в двух проекциях (прямая и правая боковая)": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

    "Врач-оториноларинголог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Врач-дерматовенеролог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Врач-стоматолог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "врач-терапевт": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "врач-профпатолог": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

    "Прививка столбняк": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка RW I вирусный гепатит В": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка RW II вирусный гепатит В": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка RW III вирусный гепатит В": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка I корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка II корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка I краснуха": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка II краснуха": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка грипп": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка ВГА": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка шигеллез": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Прививка SARS-CoV-2": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

    "Иммунный статус корь": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Иммунный статус дифтерия": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Иммунный статус столбняк": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},
    "Иммунный статус гепатит": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365)},

    "гигиеническое обучение": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365), "study_programm": "Работы, где имеется контакт с пищевыми продуктами в том числе с кремами и пр."},
    "гигиеническая аттестация": {'exists': True, 'dateLimit': datetime.now() - timedelta(days=365), "study_programm": "Работы, где имеется контакт с пищевыми продуктами в том числе с кремами и пр."},


}

if __name__ == '__main__':
    gender = 'masc'
    ELMKRequirements = ELMKRequirements(age=17, gender='masc', had_measles=True, had_rubella=True)
    print(ELMKRequirements.workWithFoodWithoutCream())

    # for key, value in TestELMK.workWithFoodWithoutCream().items():
    #     print(key, value)

