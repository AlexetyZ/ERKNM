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


def get_reasons(text_list: list):
    from not_mine import merge_both, in_one_of
    comments = {}
    # comments = {'dehyd': {'count': 'count', 'explanation': 'explanation'}}
    for text in tqdm(text_list, 'обработка...'):
        res = main(text)
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
    texts = [
        'Не в полном объеме, неверно, не в соответствии со структурой НПА отражены наименования и формулировки обязательных требований (структурные единицы ряда НПА), что свидетельствует о неправомерном расширении предмета проверки.',
        'Не в полном объеме, неверно, не в соответствии со структурой НПА отражены наименования и формулировки обязательных требований (структурные единицы ряда НПА), что свидетельствует о неправомерном расширении предмета проверки.'
    ]
    pprint(get_reasons(texts))




