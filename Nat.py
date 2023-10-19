import datetime
import re
from pprint import pprint
import Dictionary
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc,
    MorphVocab

)
from tqdm import tqdm
import multiprocessing


class Finder:
    def __init__(self, token_list):
        self.token_list = token_list


    def find_all(self, **conditions):
        result = []
        if len(conditions) > 0:
            k, v = list(conditions.items())[0]
            for token in self.token_list:
                if getattr(token, k) == v:
                    result.append(token)
            conditions.pop(k)
        else:
            return self.token_list
        if len(conditions) > 0:
            return Finder(result).find_all(**conditions)
        return result

    def findNerbyId(self, id, position: str = 'left'):
        results = {}
        for token in self.token_list:
            if getattr(token, 'head_id') == id:
                results[f'{abs(int(str(token.id).split("_")[1])-int(str(id).split("_")[1]))}'] = token
        return results[min(results)]

    def find(self, **condition):
        for token in self.token_list:
            if getattr(token, list(condition.keys())[0]) == list(condition.values())[0]:
                return token


def pattern1(token_list):
    f = Finder(token_list)
    root = f.find(rel='root')
    levels1 = f.find_all(head_id=root.id)
    for lev1 in levels1:
        print(lev1.text, f.find(head_id=lev1.id))






text = 'Исходя из ОКВЭД контролируемого лица включение в предмет КНМ соблюдение обязательных требований, предусмотренных ст. 12 Федерального закона от 30.03.1999 № 52-ФЗ «О санитарно-эпидемиологическом благополучии населения» (Санитарно-эпидемиологические требования к планировке и застройке), является излишним. 2. Статья 50 Федерального закона от 30.03.1999 № 52-ФЗ «О санитарно-эпидемиологическом благополучии населения» не содержит обязательных требований, подлежащих исполнению контролируемым лицом, в связи с чем включение данной нормы в предмет проверки является излишним. В предмете проверки указан НПА, утративший силу (ч. 2 ст. 22 ФЗ от 30.03.1999 № 52-ФЗ «О санитарно-эпидемиологическом благополучии населения»). В перечне документов, подлежащих представлению контролируемым лицом, указана излишняя и (или) не конкретизированная документация, в том числе подтверждающая соблюдение обязательных требований, фактически являющихся предметом КНМ.'







class KnowHow:
    import re
    import Dictionary

    def __init__(self, text):
        self.text = self.prepareText(text)
        # print(self.text)
        segmenter = Segmenter()
        emb = NewsEmbedding()
        morph_tagger = NewsMorphTagger(emb)
        syntax_parser = NewsSyntaxParser(emb)
        self.morph_vocab = MorphVocab()
        self.doc = Doc(self.text)
        self.doc.segment(segmenter)
        self.doc.tag_morph(morph_tagger)
        self.doc.parse_syntax(syntax_parser)
        self.sents = self.doc.sents
        self.tokens = self.doc.tokens



    def prepareText(self, text: str):
        try:
            letterBehindPoint = re.findall(r'\.\s*(\S)', text)[0]
            if letterBehindPoint:
                text = re.sub(rf'\.\s*{letterBehindPoint}', f'. {letterBehindPoint}', text)
        except:
            pass

        try:
            cypBetweenPoint = re.findall(r'\.\s*(\d)', text)[0]
            if cypBetweenPoint:
                text = re.sub(rf'\.\s*{cypBetweenPoint}', f' {cypBetweenPoint}', text)
        except:
            pass

        return text.replace('(', '').replace(')', '').replace(' – ', ' ').replace('"', '').replace("'", "")

    def finallyPreparing(self, text: str) -> str:
        try:
            text = re.sub('\.$', '', text)
        except:
            pass

        return text.strip()

    def func1(self, sent) -> str:
        finder = Finder(sent.tokens)
        root = finder.find(rel='root')
        nouns = finder.find_all(pos='NOUN')
        obls = Finder(nouns).find_all(rel='obl')
        nmods = Finder(nouns).find_all(rel='nmod')
        results = [
            *obls,
            *nmods,
            # *[v for v in Finder.find_all()],
            root
        ]

        results = sorted(results, key=lambda x: int(str(x.id).split('_')[1]))
        # print(sent.tokens)
        return ' '.join([noun.text for noun in results])

    def func3(self):
        for sent in self.sents:
            yield self.func1(sent)

    def func4(self) -> list:
        for sent in self.sents:
            # print(f"---{' '.join([token.text for token in sent.tokens])}")
            yield self.func2(sent.tokens)

    def syntezHeader(self, string: str, lemmatize: bool = True) -> str:
        hk = KnowHow(string)
        dehydrotateString = hk.func2(hk.tokens, lemmatize=lemmatize)
        if string == dehydrotateString or not dehydrotateString:
            return string
        else:
            return self.syntezHeader(dehydrotateString, lemmatize=False)

    def lemma(self, tokens):
        from natasha import MorphVocab
        morph_vocab = MorphVocab()

        for token in tokens:
            token.lemmatize(morph_vocab)

        results = [token for token in tokens]
        results = sorted(results, key=lambda x: int(str(x.id).split('_')[1]))
        # print([result.lemmatize(self.morph_vocab) for result in results])
        resultsLemma = [result.lemma for result in results]
        return self.finallyPreparing(' '.join(resultsLemma))


    def lemmatize(self) -> list:
        for sent in self.sents:
            yield self.lemma(sent.tokens)


    def func2(self, tokens, lemmatize: bool = True) -> str:

        from natasha import MorphVocab
        morph_vocab = MorphVocab()
        explanation = ' '.join([token.text for token in tokens])
        for regex, value in Dictionary.findSpecial.items():
            if re.search(regex, explanation.lower()):
                return value, value
        if lemmatize:
            for token in tokens:
                token.lemmatize(morph_vocab)
        finder = Finder(tokens)
        # print(tokens)
        roots = finder.find_all(rel='root')
        if roots:

            results = [*roots]
            for root in roots:
                r1s = finder.find_all(head_id=root.id)
                results.extend(finder.find_all(head_id=root.id))
                for r1 in r1s:
                    r2s = finder.find_all(head_id=r1.id, pos='NOUN')
                    results.extend(r2s)
                    for r2 in r2s:
                        r3s = finder.find_all(head_id=r2.id, pos='NOUN')
                        results.extend(r3s)
                        for r3 in r3s:
                            r4s = finder.find_all(head_id=r3.id, pos='NOUN')
                            results.extend(r4s)
            new_r = []
            helper = []
            for r in results:
                text = r.lemma if lemmatize else r.text
                if text not in helper:
                    new_r.append(r)
                    helper.append(text)
            results = new_r
        else:
            results = [token for token in tokens]

        results = sorted(results, key=lambda x: int(str(x.id).split('_')[1]))
        # print([result.lemmatize(self.morph_vocab) for result in results])
        resultsLemma = [result.lemma if lemmatize else result.text for result in results]
        return self.finallyPreparing(' '.join(resultsLemma)), explanation

        # print(roots)
        # r1 =finder.find_all()




    def printScheme(self, *sents):
        try:
            for sent in sents:
                print(sent[0].syntax.print())
            pass
        except Exception as ex:
            print(f'Не удалось напечатать все: {ex}')


def dehydrate(text):
    kh = KnowHow(text)
    lastVersion = kh.func2(kh.sents[0].tokens)[0]
    if lastVersion == text or not lastVersion:
        return text
    else:
        return dehydrate(lastVersion)


def multiproc_main(text):
    comments = {}
    kh = KnowHow(text)
    # kh = KnowHow('адрес наименование объект контроль не соответствовать сведение сайт указать .')
    # print(len(kh.sents))
    from not_mine import merge_both, in_one_of
    return [r for r in kh.func4()]


def main(text):
    comments = {}
    # comments = {'dehyd': {'count': 'count', 'explanation': 'explanation'}}
    kh = KnowHow(text)
    # kh = KnowHow('адрес наименование объект контроль не соответствовать сведение сайт указать .')
    # print(len(kh.sents))
    from not_mine import merge_both, in_one_of
    for r in kh.func4():

        dehydrate = r[0]
        # print(dehydrate)
        # print(dehydrate)
        commentKeyExists = in_one_of(dehydrate, list(comments.keys()))
        if dehydrate in comments:
            comments[dehydrate]['count'] += 1
        else:
            if commentKeyExists:
                comments[commentKeyExists]['count'] += 1
            else:
                comments[dehydrate] = {'count': 1, 'explanation': r[1]}


    return comments




def prepareText(text: str):
    return text.replace(';', '. ')


def get_reasons(text_list: list):
    from not_mine import merge_both, in_one_of
    comments = {}
    # comments = {'dehyd': {'count': 'count', 'explanation': 'explanation'}}
    for text in tqdm(text_list, 'обработка...'):
        res = main(prepareText(text))
        # print(res)
        for k, v in res.items():
            commentKeyExists = in_one_of(k, list(comments.keys()))
            if k in comments:
                comments[k]['count'] += v['count']
            else:
                if commentKeyExists:
                    comments[commentKeyExists]['count'] += 1
                else:
                    comments[k] = {'count': v['count'], 'explanation': v['explanation']}
    return comments


def get_reasons_multy(text_list: list):
    comments = {}
    start = datetime.datetime.now()
    pool = multiprocessing.Pool(24).imap(main, text_list)
    for dicts in pool:
        for k, v in dicts.items():
            if k in comments:
                comments[k] += v
            else:
                comments[k] = v
    print(f"ушло времени - {datetime.datetime.now()-start}")







if __name__ == '__main__':
    from Dictionary import topIsklReasons

    # for text in topIsklReasons.values():
    # print(list(KnowHow(text).func4())[0][0])
    _dict = {
        'Нарушение срока проведения проверки/непосредственного взаимодействия': 'Нарушение '
                                                                                'срока '
                                                                                'проведения '
                                                                                'проверки/непосредственного '
                                                                                'взаимодействия',

        'дубликат': 'Дублирование объекта контроля',
        'дублирование': 'Дублирование объекта контроля',
        'дублировать': 'Дублирование объекта контроля',
        'исходить лицо включение предмет кнм соблюдение ст закон благополучие население требование планировка застройка являться излишний': 'В '
                                                                                                                                            'раздел '
                                                                                                                                            'обязательные '
                                                                                                                                            'требования '
                                                                                                                                            'включены '
                                                                                                                                            'структурные '
                                                                                                                                            'подразделы '
                                                                                                                                            'НПА, '
                                                                                                                                            'не '
                                                                                                                                            'предусматривающие '
                                                                                                                                            'обязательные '
                                                                                                                                            'требования, '
                                                                                                                                            'не '
                                                                                                                                            'в '
                                                                                                                                            'полном '
                                                                                                                                            'объеме, '
                                                                                                                                            'неверно '
                                                                                                                                            'отражены '
                                                                                                                                            'структурные '
                                                                                                                                            'единицы '
                                                                                                                                            'НПА, '
                                                                                                                                            'что '
                                                                                                                                            'свидетельствует '
                                                                                                                                            'о '
                                                                                                                                            'неправомерном '
                                                                                                                                            'расширении '
                                                                                                                                            'предмета '
                                                                                                                                            'проверки.',
        'кнм нарушить срок провести': 'Нарушение срока проведения проверки/непосредственного '
                        'взаимодействия',
        'включить нпа': 'В '
                                                                                                          'раздел '
                                                                                                          'обязательные '
                                                                                                          'требования '
                                                                                                          'включены '
                                                                                                          'структурные '
                                                                                                          'подразделы '
                                                                                                          'НПА, '
                                                                                                          'не '
                                                                                                          'предусматривающие '
                                                                                                          'обязательные '
                                                                                                          'требования, '
                                                                                                          'не '
                                                                                                          'в '
                                                                                                          'полном '
                                                                                                          'объеме, '
                                                                                                          'неверно '
                                                                                                          'отражены '
                                                                                                          'структурные '
                                                                                                          'единицы '
                                                                                                          'НПА, '
                                                                                                          'что '
                                                                                                          'свидетельствует '
                                                                                                          'о '
                                                                                                          'неправомерном '
                                                                                                          'расширении '
                                                                                                          'предмета '
                                                                                                          'проверки.',
        'не указать адрес регистрация субъект': 'Строки "Адрес места нахождения", '
                                                '"Место нахождения (осуществления '
                                                'деятельности) контролируемого лица", '
                                                '"Юридический адрес" не заполнены в '
                                                'соответствии со сведениями из '
                                                'ЕГРЮЛ/ЕГРИП.',
        'необоснованно расширить предмет соблюсти требование ч ст п закон контроль постановление': 'В '
                                                                                                   'раздел '
                                                                                                   'обязательные '
                                                                                                   'требования '
                                                                                                   'включены '
                                                                                                   'структурные '
                                                                                                   'подразделы '
                                                                                                   'НПА, '
                                                                                                   'не '
                                                                                                   'предусматривающие '
                                                                                                   'обязательные '
                                                                                                   'требования, '
                                                                                                   'не '
                                                                                                   'в '
                                                                                                   'полном '
                                                                                                   'объеме, '
                                                                                                   'неверно '
                                                                                                   'отражены '
                                                                                                   'структурные '
                                                                                                   'единицы '
                                                                                                   'НПА, '
                                                                                                   'что '
                                                                                                   'свидетельствует '
                                                                                                   'о '
                                                                                                   'неправомерном '
                                                                                                   'расширении '
                                                                                                   'предмета '
                                                                                                   'проверки.',
        'неполный / неверный отображение в паспорт кнм юридический адрес хозяйствовать субъект , не совпадать с данные егрюла': 'Строки '
                                                                                                                                '"Адрес '
                                                                                                                                'места '
                                                                                                                                'нахождения", '
                                                                                                                                '"Место '
                                                                                                                                'нахождения '
                                                                                                                                '(осуществления '
                                                                                                                                'деятельности) '
                                                                                                                                'контролируемого '
                                                                                                                                'лица", '
                                                                                                                                '"Юридический '
                                                                                                                                'адрес" '
                                                                                                                                'не '
                                                                                                                                'заполнены '
                                                                                                                                'в '
                                                                                                                                'соответствии '
                                                                                                                                'со '
                                                                                                                                'сведениями '
                                                                                                                                'из '
                                                                                                                                'ЕГРЮЛ/ЕГРИП.',
        'несоблюдение установить ч 7 ст 73 закон № 248 - фз срок': 'Нарушение срока '
                                                                   'проведения '
                                                                   'проверки/непосредственного '
                                                                   'взаимодействия',
        'несоблюдение установить ч 7 ст 73 закон № 248-фз срок проведение выездной проверка в нарушение требование п 5 5 ст . 98 закон № 248-фз , п . 6 правило , утв': 'Нарушение '
                                                                                                                                                                        'срока '
                                                                                                                                                                        'проведения '
                                                                                                                                                                        'проверки/непосредственного '
                                                                                                                                                                        'взаимодействия',
        'объем отразить наименование формулировка требование единица': 'Некорректное '
                                                                       'внесение НПА, '
                                                                       'в том числе '
                                                                       'наименования '
                                                                       'и даты',
        'объем отразить формулировка требование единица': 'Некорректное внесение НПА, '
                                                          'в том числе наименования и '
                                                          'даты',
        'отсутствовать адрес место нахождение лицо': 'Строки "Адрес места '
                                                     'нахождения", "Место нахождения '
                                                     '(осуществления деятельности) '
                                                     'контролируемого лица", '
                                                     '"Юридический адрес" не '
                                                     'заполнены в соответствии со '
                                                     'сведениями из ЕГРЮЛ/ЕГРИП.',
        'план проведение не включаться мероприятие постановление особенность организация контроль': 'КНМ '
                                                                                                    'исключено '
                                                                                                    'из '
                                                                                                    'плана '
                                                                                                    'в '
                                                                                                    'силу '
                                                                                                    'Пункт '
                                                                                                    '11(3) '
                                                                                                    'постановления '
                                                                                                    'Правительства '
                                                                                                    'РФ '
                                                                                                    'от '
                                                                                                    '10.03.2022 '
                                                                                                    'N '
                                                                                                    '336.',
        'положение ст закон регулирование часть требование не распространяться лицо подлежать включение предмет': 'В '
                                                                                                                  'раздел '
                                                                                                                  'обязательные '
                                                                                                                  'требования '
                                                                                                                  'включены '
                                                                                                                  'структурные '
                                                                                                                  'подразделы '
                                                                                                                  'НПА, '
                                                                                                                  'не '
                                                                                                                  'предусматривающие '
                                                                                                                  'обязательные '
                                                                                                                  'требования, '
                                                                                                                  'не '
                                                                                                                  'в '
                                                                                                                  'полном '
                                                                                                                  'объеме, '
                                                                                                                  'неверно '
                                                                                                                  'отражены '
                                                                                                                  'структурные '
                                                                                                                  'единицы '
                                                                                                                  'НПА, '
                                                                                                                  'что '
                                                                                                                  'свидетельствует '
                                                                                                                  'о '
                                                                                                                  'неправомерном '
                                                                                                                  'расширении '
                                                                                                                  'предмета '
                                                                                                                  'проверки.',

        'предмет мероприятие указать сп санитарно-эпидемиологическ': 'В раздел '
                                                                     'обязательные '
                                                                     'требования '
                                                                     'включены '
                                                                     'структурные '
                                                                     'подразделы НПА, '
                                                                     'не '
                                                                     'предусматривающие '
                                                                     'обязательные '
                                                                     'требования, не '
                                                                     'в полном '
                                                                     'объеме, неверно '
                                                                     'отражены '
                                                                     'структурные '
                                                                     'единицы НПА, '
                                                                     'что '
                                                                     'свидетельствует '
                                                                     'о неправомерном '
                                                                     'расширении '
                                                                     'предмета '
                                                                     'проверки.',
        'пункт 11 4 постановление правительство российский федерация от 10 03 2022 № 336 в 2023 год плановый контрольный надзорный мероприятие в отношение государственный и муниципальный учреждение дошкольный и начальный общий образование , основный общий и средний общий образование не проводиться': 'КНМ '
                                                                                                                                                                                                                                                                                                             'исключено '
                                                                                                                                                                                                                                                                                                             'из '
                                                                                                                                                                                                                                                                                                             'плана '
                                                                                                                                                                                                                                                                                                             'в '
                                                                                                                                                                                                                                                                                                             'силу '
                                                                                                                                                                                                                                                                                                             'Пункт '
                                                                                                                                                                                                                                                                                                             '11(3) '
                                                                                                                                                                                                                                                                                                             'постановления '
                                                                                                                                                                                                                                                                                                             'Правительства '
                                                                                                                                                                                                                                                                                                             'РФ '
                                                                                                                                                                                                                                                                                                             'от '
                                                                                                                                                                                                                                                                                                             '10.03.2022 '
                                                                                                                                                                                                                                                                                                             'N '
                                                                                                                                                                                                                                                                                                             '336.',
        'раздел требование не сформировать подпункт пункт правило формирование план проведение мероприятие год согласование орган прокуратура включение исключение': 'В '
                                                                                                                                                                     'раздел '
                                                                                                                                                                     'обязательные '
                                                                                                                                                                     'требования '
                                                                                                                                                                     'включены '
                                                                                                                                                                     'структурные '
                                                                                                                                                                     'подразделы '
                                                                                                                                                                     'НПА, '
                                                                                                                                                                     'не '
                                                                                                                                                                     'предусматривающие '
                                                                                                                                                                     'обязательные '
                                                                                                                                                                     'требования, '
                                                                                                                                                                     'не '
                                                                                                                                                                     'в '
                                                                                                                                                                     'полном '
                                                                                                                                                                     'объеме, '
                                                                                                                                                                     'неверно '
                                                                                                                                                                     'отражены '
                                                                                                                                                                     'структурные '
                                                                                                                                                                     'единицы '
                                                                                                                                                                     'НПА, '
                                                                                                                                                                     'что '
                                                                                                                                                                     'свидетельствует '
                                                                                                                                                                     'о '
                                                                                                                                                                     'неправомерном '
                                                                                                                                                                     'расширении '
                                                                                                                                                                     'предмета '
                                                                                                                                                                     'проверки.',
        'санпин 3 3686-21 01.2001': 'В раздел обязательные требования включены '
                                    'структурные подразделы НПА, не предусматривающие '
                                    'обязательные требования, не в полном объеме, '
                                    'неверно отражены структурные единицы НПА, что '
                                    'свидетельствует о неправомерном расширении '
                                    'предмета проверки.',
        'статья закон благополучие население не содержать требование что включение норма предмет проверка являться излишний': 'В '
                                                                                                                              'раздел '
                                                                                                                              'обязательные '
                                                                                                                              'требования '
                                                                                                                              'включены '
                                                                                                                              'структурные '
                                                                                                                              'подразделы '
                                                                                                                              'НПА, '
                                                                                                                              'не '
                                                                                                                              'предусматривающие '
                                                                                                                              'обязательные '
                                                                                                                              'требования, '
                                                                                                                              'не '
                                                                                                                              'в '
                                                                                                                              'полном '
                                                                                                                              'объеме, '
                                                                                                                              'неверно '
                                                                                                                              'отражены '
                                                                                                                              'структурные '
                                                                                                                              'единицы '
                                                                                                                              'НПА, '
                                                                                                                              'что '
                                                                                                                              'свидетельствует '
                                                                                                                              'о '
                                                                                                                              'неправомерном '
                                                                                                                              'расширении '
                                                                                                                              'предмета '
                                                                                                                              'проверки.',
        'требование значительно шире перечень акт': 'В раздел обязательные требования '
                                                    'включены структурные подразделы '
                                                    'НПА, не предусматривающие '
                                                    'обязательные требования, не в '
                                                    'полном объеме, неверно отражены '
                                                    'структурные единицы НПА, что '
                                                    'свидетельствует о неправомерном '
                                                    'расширении предмета проверки.',
        'требование мероприятие 04.2021 не указать единица акт надзор': 'Некорректное '
                                                                        'внесение '
                                                                        'НПА, в том '
                                                                        'числе '
                                                                        'наименования '
                                                                        'и даты',
        'указать информация основание включение мероприятие план проверка год еркнм отсутствовать сведение': 'Неверно '
                                                                                                             'выбрано '
                                                                                                             'основание '
                                                                                                             'проведения '
                                                                                                             'КНМ',

        'управление область не указать категория риск': 'Категория риска не '
                                                        'подтверждена или не отнесена '
                                                        'к категории чрезвычайно '
                                                        'высокого и высокого рисков',

        'Нарушение срока проведения проверки/непосредственного взаимодействия': 'Нарушение '
                                                                                'срока '
                                                                                'проведения '
                                                                                'проверки/непосредственного '
                                                                                'взаимодействия',


        'в нарушение ст 15 федеральный закон № 248-фз в раздел обязательный требование включить нпа , не входить в перечень нпа , содержать обязательный требование , оценка соблюдение который осуществляться в рамка данный вид контроль нпа № санпин 2 2 1/2 1 1 1200-03 от 25.09 2003 санитарно-защитный зона и санитарный классификация предприятие , сооружение и иной объект - данный нпа с указать дата принятие не существовать': 'В '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'раздел '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'требования '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'включены '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'подразделы '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'не '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'предусматривающие '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'требования, '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'не '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'в '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'полном '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'объеме, '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'неверно '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'отражены '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'единицы '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'что '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'свидетельствует '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'о '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'неправомерном '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'расширении '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'предмета '
                                                                                                                                                                                                                                                                                                                                                                                                                                           'проверки.',
        'в паспорт кнм срок непосредственный взаимодействие с контролировать лицо - субъект смп превышать срок , установить закон срок проверка превышать предусмотреть часть 7 статья 73 федеральный закон № 248-фз': 'Нарушение '
                                                                                                                                                                                                                       'срока '
                                                                                                                                                                                                                       'проведения '
                                                                                                                                                                                                                       'проверки/непосредственного '
                                                                                                                                                                                                                       'взаимодействия',
        'в план проведение плановый контрольный надзорный мероприятие до 2030 год не включаться плановый контрольный надзорный мероприятие в отношение государственный и муниципальный учреждение дошкольный и начальный общий образование , основный общий и средний общий образование , объект контроль который отнести к категория чрезвычайно высокий и высокий риск п 114 постановление правительство рф от 10 03.2022 n 336 о особенность организация и осуществление государственный контроль надзор , муниципальный контроль': 'КНМ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'исключено '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'из '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'плана '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'в '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'силу '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'Пункт '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       '11(3) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'постановления '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'Правительства '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'РФ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'от '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       '10.03.2022 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'N '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       '336.',
        'в предмет контрольный надзорный мероприятие указать сп 3 1/2 4.3598-20 « санитарно-эпидемиологическ': 'В '
                                                                                                               'раздел '
                                                                                                               'обязательные '
                                                                                                               'требования '
                                                                                                               'включены '
                                                                                                               'структурные '
                                                                                                               'подразделы '
                                                                                                               'НПА, '
                                                                                                               'не '
                                                                                                               'предусматривающие '
                                                                                                               'обязательные '
                                                                                                               'требования, '
                                                                                                               'не '
                                                                                                               'в '
                                                                                                               'полном '
                                                                                                               'объеме, '
                                                                                                               'неверно '
                                                                                                               'отражены '
                                                                                                               'структурные '
                                                                                                               'единицы '
                                                                                                               'НПА, '
                                                                                                               'что '
                                                                                                               'свидетельствует '
                                                                                                               'о '
                                                                                                               'неправомерном '
                                                                                                               'расширении '
                                                                                                               'предмета '
                                                                                                               'проверки.',
        'весь положение ч 3 ст 23 федеральный закон от 27.12 2002 № 184-фз « о технический регулирование » в часть обязательный требование , устанавливать порядок формирование и ведение реестр сертификат соответствие и декларация о соответствие , в тот число внесение в он сведение , не распространяться на контролировать лицо , а соответственно не подлежать включение в предмет кнм': 'В '
                                                                                                                                                                                                                                                                                                                                                                                                 'раздел '
                                                                                                                                                                                                                                                                                                                                                                                                 'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                 'требования '
                                                                                                                                                                                                                                                                                                                                                                                                 'включены '
                                                                                                                                                                                                                                                                                                                                                                                                 'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                 'подразделы '
                                                                                                                                                                                                                                                                                                                                                                                                 'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                 'не '
                                                                                                                                                                                                                                                                                                                                                                                                 'предусматривающие '
                                                                                                                                                                                                                                                                                                                                                                                                 'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                 'требования, '
                                                                                                                                                                                                                                                                                                                                                                                                 'не '
                                                                                                                                                                                                                                                                                                                                                                                                 'в '
                                                                                                                                                                                                                                                                                                                                                                                                 'полном '
                                                                                                                                                                                                                                                                                                                                                                                                 'объеме, '
                                                                                                                                                                                                                                                                                                                                                                                                 'неверно '
                                                                                                                                                                                                                                                                                                                                                                                                 'отражены '
                                                                                                                                                                                                                                                                                                                                                                                                 'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                 'единицы '
                                                                                                                                                                                                                                                                                                                                                                                                 'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                 'что '
                                                                                                                                                                                                                                                                                                                                                                                                 'свидетельствует '
                                                                                                                                                                                                                                                                                                                                                                                                 'о '
                                                                                                                                                                                                                                                                                                                                                                                                 'неправомерном '
                                                                                                                                                                                                                                                                                                                                                                                                 'расширении '
                                                                                                                                                                                                                                                                                                                                                                                                 'предмета '
                                                                                                                                                                                                                                                                                                                                                                                                 'проверки.',

        'вопреки требование п 11 4 пп 336': 'КНМ исключено из плана в силу Пункт '
                                            '11(3) постановления Правительства РФ от '
                                            '10.03.2022 N 336.',
        'вопреки требование п 11 правило формирование и ведение единый реестр контрольный надзорный мероприятие , утвердить постановление правительство российский федерация от 16 04.2021 № 604 далее правило № 604 в паспорт кнм не указать структурный единица нормативный правовой акт , предусматривать обязательный требование , оценка соблюдение который осуществляться в рамка контроль надзор': 'Некорректное '
                                                                                                                                                                                                                                                                                                                                                                                                          'внесение '
                                                                                                                                                                                                                                                                                                                                                                                                          'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                          'в '
                                                                                                                                                                                                                                                                                                                                                                                                          'том '
                                                                                                                                                                                                                                                                                                                                                                                                          'числе '
                                                                                                                                                                                                                                                                                                                                                                                                          'наименования '
                                                                                                                                                                                                                                                                                                                                                                                                          'и '
                                                                                                                                                                                                                                                                                                                                                                                                          'даты',
        'исходить из оквэда контролировать лицо включение в предмет кнм соблюдение обязательный требование , предусмотреть ст 12 федеральный закон от 30 03 1999 № 52-фз « о санитарно-эпидемиологический благополучие население » санитарно-эпидемиологический требование к планировка и застройка , являться излишний': 'В '
                                                                                                                                                                                                                                                                                                                          'раздел '
                                                                                                                                                                                                                                                                                                                          'обязательные '
                                                                                                                                                                                                                                                                                                                          'требования '
                                                                                                                                                                                                                                                                                                                          'включены '
                                                                                                                                                                                                                                                                                                                          'структурные '
                                                                                                                                                                                                                                                                                                                          'подразделы '
                                                                                                                                                                                                                                                                                                                          'НПА, '
                                                                                                                                                                                                                                                                                                                          'не '
                                                                                                                                                                                                                                                                                                                          'предусматривающие '
                                                                                                                                                                                                                                                                                                                          'обязательные '
                                                                                                                                                                                                                                                                                                                          'требования, '
                                                                                                                                                                                                                                                                                                                          'не '
                                                                                                                                                                                                                                                                                                                          'в '
                                                                                                                                                                                                                                                                                                                          'полном '
                                                                                                                                                                                                                                                                                                                          'объеме, '
                                                                                                                                                                                                                                                                                                                          'неверно '
                                                                                                                                                                                                                                                                                                                          'отражены '
                                                                                                                                                                                                                                                                                                                          'структурные '
                                                                                                                                                                                                                                                                                                                          'единицы '
                                                                                                                                                                                                                                                                                                                          'НПА, '
                                                                                                                                                                                                                                                                                                                          'что '
                                                                                                                                                                                                                                                                                                                          'свидетельствует '
                                                                                                                                                                                                                                                                                                                          'о '
                                                                                                                                                                                                                                                                                                                          'неправомерном '
                                                                                                                                                                                                                                                                                                                          'расширении '
                                                                                                                                                                                                                                                                                                                          'предмета '
                                                                                                                                                                                                                                                                                                                          'проверки.',


        'не в полный объем отразить наименование и формулировка обязательный требование структурный единица нпа': 'Некорректное '
                                                                                                                  'внесение '
                                                                                                                  'НПА, '
                                                                                                                  'в '
                                                                                                                  'том '
                                                                                                                  'числе '
                                                                                                                  'наименования '
                                                                                                                  'и '
                                                                                                                  'даты',
        'не в полный объем отразить формулировка обязательный требование структурный единица нпа': 'Некорректное '
                                                                                                   'внесение '
                                                                                                   'НПА, '
                                                                                                   'в '
                                                                                                   'том '
                                                                                                   'числе '
                                                                                                   'наименования '
                                                                                                   'и '
                                                                                                   'даты',

        'не указать адрес регистрация юридический адрес хозяйствовать субъект': 'Строки '
                                                                                '"Адрес '
                                                                                'места '
                                                                                'нахождения", '
                                                                                '"Место '
                                                                                'нахождения '
                                                                                '(осуществления '
                                                                                'деятельности) '
                                                                                'контролируемого '
                                                                                'лица", '
                                                                                '"Юридический '
                                                                                'адрес" '
                                                                                'не '
                                                                                'заполнены '
                                                                                'в '
                                                                                'соответствии '
                                                                                'со '
                                                                                'сведениями '
                                                                                'из '
                                                                                'ЕГРЮЛ/ЕГРИП.',
        'необоснованно расширить предмет кнм , не соблюсти требование ч 3 ст . 7 , п . 1 ст 37 , п . 1 ч . 1 ст . 15 федеральный закон от 34.07.2020 № 248-фз « о государственный контроль надзор и муниципальный контроль в российский федерация » , п . 11 постановление правительство рф от 16.04.2021 № 604': 'В '
                                                                                                                                                                                                                                                                                                                  'раздел '
                                                                                                                                                                                                                                                                                                                  'обязательные '
                                                                                                                                                                                                                                                                                                                  'требования '
                                                                                                                                                                                                                                                                                                                  'включены '
                                                                                                                                                                                                                                                                                                                  'структурные '
                                                                                                                                                                                                                                                                                                                  'подразделы '
                                                                                                                                                                                                                                                                                                                  'НПА, '
                                                                                                                                                                                                                                                                                                                  'не '
                                                                                                                                                                                                                                                                                                                  'предусматривающие '
                                                                                                                                                                                                                                                                                                                  'обязательные '
                                                                                                                                                                                                                                                                                                                  'требования, '
                                                                                                                                                                                                                                                                                                                  'не '
                                                                                                                                                                                                                                                                                                                  'в '
                                                                                                                                                                                                                                                                                                                  'полном '
                                                                                                                                                                                                                                                                                                                  'объеме, '
                                                                                                                                                                                                                                                                                                                  'неверно '
                                                                                                                                                                                                                                                                                                                  'отражены '
                                                                                                                                                                                                                                                                                                                  'структурные '
                                                                                                                                                                                                                                                                                                                  'единицы '
                                                                                                                                                                                                                                                                                                                  'НПА, '
                                                                                                                                                                                                                                                                                                                  'что '
                                                                                                                                                                                                                                                                                                                  'свидетельствует '
                                                                                                                                                                                                                                                                                                                  'о '
                                                                                                                                                                                                                                                                                                                  'неправомерном '
                                                                                                                                                                                                                                                                                                                  'расширении '
                                                                                                                                                                                                                                                                                                                  'предмета '
                                                                                                                                                                                                                                                                                                                  'проверки.',


        'несоблюдение установить ч 7 ст 73 федеральный закон от 31.07.2020 № 248-фз срок проведение выездной проверка 10 рабочий день , в тот число срок непосредственный взаимодействие в отношение субъект малый предпринимательство 50 час для малый предприятие и 15 час для микропредприятие': 'Нарушение '
                                                                                                                                                                                                                                                                                                    'срока '
                                                                                                                                                                                                                                                                                                    'проведения '
                                                                                                                                                                                                                                                                                                    'проверки/непосредственного '
                                                                                                                                                                                                                                                                                                    'взаимодействия',
        'несоблюдение установить ч 7 ст 73 федеральный закон № 248 срок проведение выездной проверка , в частность срок непосредственный взаимодействие в отношение субъект малый предпринимательство': 'Нарушение '
                                                                                                                                                                                                        'срока '
                                                                                                                                                                                                        'проведения '
                                                                                                                                                                                                        'проверки/непосредственного '
                                                                                                                                                                                                        'взаимодействия',
        'несоблюдение установить ч 7 ст 73 федеральный закон № 248-фз срок непосредственный взаимодействие в отношение субъект малый предпринимательство 15 час для микропредприятие': 'Нарушение '
                                                                                                                                                                                       'срока '
                                                                                                                                                                                       'проведения '
                                                                                                                                                                                       'проверки/непосредственного '
                                                                                                                                                                                       'взаимодействия',
        'несоблюдение установить ч 7 ст 73 федеральный закон № 248-фз срок проведение выездной проверка , в тот число срок непосредственный взаимодействие в отношение субъект малый предпринимательство': 'Нарушение '
                                                                                                                                                                                                           'срока '
                                                                                                                                                                                                           'проведения '
                                                                                                                                                                                                           'проверки/непосредственного '
                                                                                                                                                                                                           'взаимодействия',
        'несоблюдение установить ч 7 ст 73 федеральный закон № 248-фз срок проведение выездной проверка 10 рабочий день , в тот число , срок непосредственный взаимодействие в отношение малый предприятие 50 час': 'Нарушение '
                                                                                                                                                                                                                    'срока '
                                                                                                                                                                                                                    'проведения '
                                                                                                                                                                                                                    'проверки/непосредственного '
                                                                                                                                                                                                                    'взаимодействия',

        'обязательный требование , подлежать проверка предмет контрольный надзорный мероприятие значительно шире перечень проверять нормативный акт указать в применять проверочный лист': 'В '
                                                                                                                                                                                           'раздел '
                                                                                                                                                                                           'обязательные '
                                                                                                                                                                                           'требования '
                                                                                                                                                                                           'включены '
                                                                                                                                                                                           'структурные '
                                                                                                                                                                                           'подразделы '
                                                                                                                                                                                           'НПА, '
                                                                                                                                                                                           'не '
                                                                                                                                                                                           'предусматривающие '
                                                                                                                                                                                           'обязательные '
                                                                                                                                                                                           'требования, '
                                                                                                                                                                                           'не '
                                                                                                                                                                                           'в '
                                                                                                                                                                                           'полном '
                                                                                                                                                                                           'объеме, '
                                                                                                                                                                                           'неверно '
                                                                                                                                                                                           'отражены '
                                                                                                                                                                                           'структурные '
                                                                                                                                                                                           'единицы '
                                                                                                                                                                                           'НПА, '
                                                                                                                                                                                           'что '
                                                                                                                                                                                           'свидетельствует '
                                                                                                                                                                                           'о '
                                                                                                                                                                                           'неправомерном '
                                                                                                                                                                                           'расширении '
                                                                                                                                                                                           'предмета '
                                                                                                                                                                                           'проверки.',

        'отсутствовать адрес место нахождение юридический лицо': 'Строки "Адрес места '
                                                                 'нахождения", "Место '
                                                                 'нахождения '
                                                                 '(осуществления '
                                                                 'деятельности) '
                                                                 'контролируемого '
                                                                 'лица", "Юридический '
                                                                 'адрес" не заполнены '
                                                                 'в соответствии со '
                                                                 'сведениями из '
                                                                 'ЕГРЮЛ/ЕГРИП.',

        'постановление главный гос . сан . врач от 30 06 2020 № 16': 'В раздел '
                                                                     'обязательные '
                                                                     'требования '
                                                                     'включены '
                                                                     'структурные '
                                                                     'подразделы НПА, '
                                                                     'не '
                                                                     'предусматривающие '
                                                                     'обязательные '
                                                                     'требования, не '
                                                                     'в полном '
                                                                     'объеме, неверно '
                                                                     'отражены '
                                                                     'структурные '
                                                                     'единицы НПА, '
                                                                     'что '
                                                                     'свидетельствует '
                                                                     'о неправомерном '
                                                                     'расширении '
                                                                     'предмета '
                                                                     'проверки.',
        'постановление минздрав россия от 13 06.2001 № 18 « о введение в действие сп 1.1.1058-01 » . приказ минздрав россия от 06.12.2021 № 1122 н « о утверждение национальный календарь профилактический прививка , календарь профилактический прививка по эпидемический показание и порядка проведение профилактический прививка » . указать в полный объем тр тс 005/2011 , тртс 021/2011 , тртс 023/2011 , тртс 033/2013 , тртс 034/2013 , тр еаэс 040/2016 , тр еаэс 044/2017 , тогда как перечень они предусмотреть только в часть с исключение , при это не указать содержание данные нпа': 'В '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'раздел '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'требования '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'включены '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'подразделы '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'не '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'предусматривающие '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'обязательные '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'требования, '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'не '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'в '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'полном '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'объеме, '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'неверно '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'отражены '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'структурные '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'единицы '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'НПА, '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'что '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'свидетельствует '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'о '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'неправомерном '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'расширении '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'предмета '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'проверки.',

        'предыдущий кнм провести с по': 'Нарушение срока проведения '
                                        'проверки/непосредственного взаимодействия',

        'раздел « обязательный требование » не сформировать в соответствие с подпункт « в » пункт 8 правило формирование план проведение плановый контрольный надзорный мероприятие на очередной календарный год , он согласование с орган прокуратура , включение в он и исключение из он контрольный надзорный мероприятие в течение год , утвердить постановление править': 'В '
                                                                                                                                                                                                                                                                                                                                                                               'раздел '
                                                                                                                                                                                                                                                                                                                                                                               'обязательные '
                                                                                                                                                                                                                                                                                                                                                                               'требования '
                                                                                                                                                                                                                                                                                                                                                                               'включены '
                                                                                                                                                                                                                                                                                                                                                                               'структурные '
                                                                                                                                                                                                                                                                                                                                                                               'подразделы '
                                                                                                                                                                                                                                                                                                                                                                               'НПА, '
                                                                                                                                                                                                                                                                                                                                                                               'не '
                                                                                                                                                                                                                                                                                                                                                                               'предусматривающие '
                                                                                                                                                                                                                                                                                                                                                                               'обязательные '
                                                                                                                                                                                                                                                                                                                                                                               'требования, '
                                                                                                                                                                                                                                                                                                                                                                               'не '
                                                                                                                                                                                                                                                                                                                                                                               'в '
                                                                                                                                                                                                                                                                                                                                                                               'полном '
                                                                                                                                                                                                                                                                                                                                                                               'объеме, '
                                                                                                                                                                                                                                                                                                                                                                               'неверно '
                                                                                                                                                                                                                                                                                                                                                                               'отражены '
                                                                                                                                                                                                                                                                                                                                                                               'структурные '
                                                                                                                                                                                                                                                                                                                                                                               'единицы '
                                                                                                                                                                                                                                                                                                                                                                               'НПА, '
                                                                                                                                                                                                                                                                                                                                                                               'что '
                                                                                                                                                                                                                                                                                                                                                                               'свидетельствует '
                                                                                                                                                                                                                                                                                                                                                                               'о '
                                                                                                                                                                                                                                                                                                                                                                               'неправомерном '
                                                                                                                                                                                                                                                                                                                                                                               'расширении '
                                                                                                                                                                                                                                                                                                                                                                               'предмета '
                                                                                                                                                                                                                                                                                                                                                                               'проверки.',


        'санпин 3 3686-21 от 28 01.2001': 'В раздел обязательные требования включены '
                                          'структурные подразделы НПА, не '
                                          'предусматривающие обязательные требования, '
                                          'не в полном объеме, неверно отражены '
                                          'структурные единицы НПА, что '
                                          'свидетельствует о неправомерном расширении '
                                          'предмета проверки.',
        'статья 50 федеральный закон от 30 03 1999 № 52-фз « о санитарно-эпидемиологический благополучие население » не содержать обязательный требование , подлежать исполнение контролировать лицо , в связь с что включение данный норма в предмет проверка являться излишний': 'В '
                                                                                                                                                                                                                                                                                   'раздел '
                                                                                                                                                                                                                                                                                   'обязательные '
                                                                                                                                                                                                                                                                                   'требования '
                                                                                                                                                                                                                                                                                   'включены '
                                                                                                                                                                                                                                                                                   'структурные '
                                                                                                                                                                                                                                                                                   'подразделы '
                                                                                                                                                                                                                                                                                   'НПА, '
                                                                                                                                                                                                                                                                                   'не '
                                                                                                                                                                                                                                                                                   'предусматривающие '
                                                                                                                                                                                                                                                                                   'обязательные '
                                                                                                                                                                                                                                                                                   'требования, '
                                                                                                                                                                                                                                                                                   'не '
                                                                                                                                                                                                                                                                                   'в '
                                                                                                                                                                                                                                                                                   'полном '
                                                                                                                                                                                                                                                                                   'объеме, '
                                                                                                                                                                                                                                                                                   'неверно '
                                                                                                                                                                                                                                                                                   'отражены '
                                                                                                                                                                                                                                                                                   'структурные '
                                                                                                                                                                                                                                                                                   'единицы '
                                                                                                                                                                                                                                                                                   'НПА, '
                                                                                                                                                                                                                                                                                   'что '
                                                                                                                                                                                                                                                                                   'свидетельствует '
                                                                                                                                                                                                                                                                                   'о '
                                                                                                                                                                                                                                                                                   'неправомерном '
                                                                                                                                                                                                                                                                                   'расширении '
                                                                                                                                                                                                                                                                                   'предмета '
                                                                                                                                                                                                                                                                                   'проверки.',


        'указать недостоверный неполный информация о основание включение контрольно-надзорный мероприятие в план проверка на 2024 год в еркнм отсутствовать сведение о ранее провести плановый кнм': 'Неверно '
                                                                                                                                                                                                     'выбрано '
                                                                                                                                                                                                     'основание '
                                                                                                                                                                                                     'проведения '
                                                                                                                                                                                                     'КНМ',
        'указать ссылка на решение комиссия таможенный союз от 28 05 2010 № 299 с некорректный наименование нпа': 'Некорректное '
                                                                                                                  'внесение '
                                                                                                                  'НПА, '
                                                                                                                  'в '
                                                                                                                  'том '
                                                                                                                  'числе '
                                                                                                                  'наименования '
                                                                                                                  'и '
                                                                                                                  'даты',

        'управление роспотребнадзор по самарский область не указать категория риск': 'Категория '
                                                                                     'риска '
                                                                                     'не '
                                                                                     'подтверждена '
                                                                                     'или '
                                                                                     'не '
                                                                                     'отнесена '
                                                                                     'к '
                                                                                     'категории '
                                                                                     'чрезвычайно '
                                                                                     'высокого '
                                                                                     'и '
                                                                                     'высокого '
                                                                                     'рисков'




    }
    _dict4 = {
        0: 'В раздел обязательные требования включены структурные подразделы НПА, не '
           'предусматривающие обязательные требования, не в полном объеме, неверно '
           'отражены структурные единицы НПА, что свидетельствует о неправомерном '
           'расширении предмета проверки.',
        1: 'В перечне документов, подлежащих представлению контролируемым лицом, '
           'указана излишняя и (или) не конкретизированная документация, в том числе '
           'ограничение на истребование которой установлено п. 6 ст. 37 Федерального '
           'закона от 31.07.2020 № 248-ФЗ «О государственном контроле (надзоре) и '
           'муниципальном контроле в Российской Федерации» (правоустанавливающие и '
           'иные док-ты, сведения о проверяемом юридическом лице, фото, видео '
           'материалы и др.), а также подтверждающая соблюдение обязательных '
           'требований, фактически являющихся предметом КНМ.',
        2: 'Нет сведений/неполные/недостоверные сведения об объекте в ЕРВК',
        3: 'Строки "Адрес места нахождения", "Место нахождения (осуществления '
           'деятельности) контролируемого лица", "Юридический адрес" не заполнены в '
           'соответствии со сведениями из ЕГРЮЛ/ЕГРИП.',
        4: 'КНМ исключено из плана в силу Пункт 11(3) постановления Правительства РФ '
           'от 10.03.2022 N 336.',
        5: 'Нарушение срока проведения проверки/непосредственного взаимодействия',
        6: 'Ошибка заполнения мест проведения контрольного (надзорного) мероприятия',
        7: 'Некорректное внесение НПА, в том числе наименования и даты',
        8: 'Дублирование объекта контроля',
        9: 'Неверно выбрано основание проведения КНМ',
        10: 'Запланированные в рамках плановой выездной проверки контрольные '
            '(надзорные) действия подлежат осуществлению в рамках менее '
            'обременительного для контролируемого лица иного контрольного '
            '(надзорного) мероприятия, предусмотренного п. 70 Положения  № 1100, что '
            'не отвечает требованию  п. 2 ч. 3 ст. 73 Федерального закона № 248-ФЗ',
        11: 'В силу постановления Правительства РФ от 08.09.2021 №1520 введен '
            'мораторий на плановые проверки в отношении субъектов малого бизнеса.',
        12: 'Категория риска не подтверждена или не отнесена к категории чрезвычайно '
            'высокого и высокого рисков',
        13: 'Строки "Адрес места нахождения", "Место нахождения (осуществления '
            'деятельности) контролируемого лица", "Юридический адрес" не заполнены в '
            'соответствии со сведениями из ЕГРЮЛ/ЕГРИП.',
        14: 'В раздел обязательные требования включены структурные подразделы НПА, не '
            'предусматривающие обязательные требования, не в полном объеме, неверно '
            'отражены структурные единицы НПА, что свидетельствует о неправомерном '
            'расширении предмета проверки.'
    }

    _dict2 = {
        'СанПин 3.3686-21 от 28 01.2001': 0,
        'Постановление Главного гос . сан . врача от 30 06.2020 № 16': 0,
        'Указана ссылка на решение Комиссии Таможенного союза от 28 05.2010 № 299 с некорректным наименованием НПА': 7,
        'Предыдущее КНМ проведено с  по ': 5,
        'Неполное / неверное отображение в паспорте КНМ юридического адреса хозяйствующего субъекта , не совпадающее с данными ЕГРЮЛ': 3,
        'Исходя из ОКВЭД контролируемого лица включение в предмет КНМ соблюдение обязательных требований , предусмотренных ст 12 Федерального закона от 30.03 1999 № 52-ФЗ « О санитарно-эпидемиологическом благополучии населения » Санитарно-эпидемиологические требования к планировке и застройке , является излишним': 0,
        'Статья 50 Федерального закона от 30.03 1999 № 52-ФЗ « О санитарно-эпидемиологическом благополучии населения » не содержит обязательных требований , подлежащих исполнению контролируемым лицом , в связи с чем включение данной нормы в предмет проверки является излишним': 0,
        'Все положения ч 3 ст . 23 Федерального закона от 27.12.2002 № 184-ФЗ « О техническом регулировании » в части обязательных требований , устанавливающих порядок формирования и ведения реестра сертификатов соответствия и деклараций о соответствии , в том числе внесения в него сведений , не распространяются на контролируемое лицо , а соответственно не подлежат включению в предмет КНМ': 0,
        'Не указан адрес регистрации юридический адрес хозяйствующего субъекта': 3,
        'Несоблюдение установленного ч . 7 ст . 73 Федерального закона от 31.07.2020 № 248-ФЗ срока проведения выездной проверки 10 рабочих дней , в том числе срока непосредственного взаимодействий в отношении субъекта малого предпринимательства 50 часов для малого предприятия и 15 часов для микропредприятия': 5,
        'вопреки требованию п 11 Правил формирования и ведения единого реестра контрольных надзорных мероприятий , утверждённых Постановлением Правительства Российской Федерации от 16.04.2021 № 604 далее Правила № 604 в паспорте КНМ не указаны структурные единицы нормативного правового акта , предусматривающего обязательные требования , оценка соблюдения которых осуществляется в рамках контроля надзор': 7,
        # 'в нарушение требований п 5 5 ст . 98 Федерального закона № 248-ФЗ и п . 6 Правил № 2428 сведения об об': 2,   # Не вносить после func4!!!!!
        'Несоблюдение установленного ч 7 ст 73 Закона № 248-ФЗ срока проведения выездной проверки В нарушение требований п . 5.5 ст . 98 Закона № 248-ФЗ , п . 6 правил , утв .': 5,
        'Несоблюдение установленного ч 7 ст 73 Федерального закона № 248-ФЗ срока непосредственного взаимодействия в отношении субъекта малого предпринимательства 15 часов для микропредприятия': 5,
        'отсутствует адрес места нахождения юридического лица': 3,
        'необоснованно расширен предмет КНМ , не соблюдены требования ч . 3 ст . 7 , п . 1 ст . 37 , п . 1 ч . 1 ст . 15 Федерального закона от 34.07.2020 № 248-ФЗ « О государственном контроле надзоре и муниципальном контроле в Российской Федерации » , п . 11 постановления Правительства РФ от 16.04.2021 № 604': 0,
        'Постановление Минздрава России от 13.06.2001 № 18 « О введении в действие СП 1.1.1058-01 » . приказ Минздрава России от 06.12.2021 № 1122 н « Об утверждении национального календаря профилактических прививок , календаря профилактических прививок по эпидемическим показаниям и порядка проведения профилактических прививок » . указаны в полном объеме ТР ТС 005/2011 , ТРТС 021/2011 , ТРТС 023/2011 , ТРТС 033/2013 , ТРТС 034/2013 , ТР ЕАЭС 040/2016 , ТР ЕАЭС 044/2017 , тогда как перечнем они предусмотрены только в части с исключениями , при этом не указано содержание данных НПА': 0,
        'Вопреки требованиям п 11 (4) ПП 336': 4,
        'пунктом 11 4 постановления Правительства Российской Федерации от 10 03.2022 № 336 в 2023 году плановые контрольные надзорные мероприятия в отношении государственных и муниципальных учреждений дошкольного и начального общего образования , основного общего и среднего общего образования не проводятся': 4,
        'В паспорте КНМ срок непосредственного взаимодействия с контролируемым лицом - субъектом СМП превышает срок , установленный законом срок проверки превышает предусмотренный частью 7 статьи 73 Федерального закона № 248-ФЗ': 5,
        'указана недостоверная неполная информация об основании включения контрольно-надзорного мероприятия в план проверок на 2024 год в ЕРКНМ отсутствуют сведения о ранее проведенных плановых КНМ': 9,
        'Раздел « Обязательные требования » не сформирован в соответствии с подпунктом « в » пункта 8 Правил формирования плана проведения плановых контрольных надзорных мероприятий на очередной календарный год , его согласования с органами прокуратуры , включения в него и исключения из него контрольных надзорных мероприятий в течение года , утвержденных постановлением Правит': 0,
        'В нарушении ст 15 Федерального закона № 248-ФЗ в раздел Обязательные требования включены НПА , не входящие в перечень НПА , содержащих обязательные требования , оценка соблюдения которых осуществляется в рамках данного вида контроля НПА № СанПиН 2.2 1/2 1 1 1200-03 от 25.09.2003 Санитарно-защитные зоны и санитарная классификация предприятий , сооружений и иных объектов - данного НПА с указанной датой принятия не существует': 0,
        'Несоблюдение установленного ч 7 ст 73 Федерального закона № 248-ФЗ срока проведения выездной проверки , в том числе срока непосредственного взаимодействия в отношении субъекта малого предпринимательства': 5,
        'Несоблюдение установленного ч 7 ст 73 Федерального закона № 248-ФЗ срока проведения выездной проверки 10 рабочих дней , в том числе , срока непосредственного взаимодействия в отношении малого предприятия 50 часов .': 5,
        'дубликат': 8,
        'дублирование': 8,
        'дублирован': 8,
        'В предмете контрольного надзорного мероприятия указаны СП 3 1/2.4.3598-20 « Санитарно-эпидемиологически': 0,
        'Обязательные требования , подлежащие проверке предмет контрольного надзорного мероприятия значительно шире перечня проверяемых нормативных актов указанных в применяемых проверочных листах': 0,
        'не в полном объеме отражены наименования и формулировки обязательных требований структурные единицы НПА': 7,

        'Не в полном объеме отражены формулировки обязательных требований структурные единицы НПА': 7,
        'Управлением Роспотребнадзора по Самарской области не указана категория риска': 12,
        'Несоблюдение установленного ч 7 ст 73 Федерального закона № 248 срока проведения выездной проверки , в частности срока непосредственного взаимодействия в отношении субъектов малого предпринимательства .': 5,
        'Несоблюдение установленного ч 7 ст 73 Закона № 248 - ФЗ срока': 5,
        'В планы проведения плановых контрольных надзорных мероприятий до 2030 года не включаются плановые контрольные надзорные мероприятия в отношении государственных и муниципальных учреждений дошкольного и начального общего образования , основного общего и среднего общего образования , объекты контроля которых отнесены к категориям чрезвычайно высокого и высокого риска п 114 Постановление Правительства РФ от 10.03.2022 N 336 Об особенностях организации и осуществления государственного контроля надзора , муниципального контроля': 4,









    }
    # for k, val in tqdm(_dict2.items()):
    #     _dict[list(KnowHow(k).lemmatize())[0]] = _dict4[val]

    pprint(_dict)



