import json

list = [
    {'actCreateDate': None, 'actCreateDateEn': None, 'addresses': [], 'admLevelId': 50001, 'appealed': False,
     'approveDocOrderDate': '02.02.2022', 'approveDocOrderNum': '76-ВН', 'approveDocRequestDate': None,
     'approveDocRequestNum': None, 'approveDocs': [], 'approveRequired': False, 'approved': None, 'approvedErknm': None,
     'chlistCount': 0, 'chlistFilledCount': 0, 'chlistFillingIndicationTypeId': [], 'collaboratingOrganizations': [],
     'collaboratingOrganizationsIds': [], 'comment': None,
     'controllingOrganization': 'Управление Роспотребнадзора по Кемеровской области ',
     'controllingOrganizationId': 10001011723, 'createPlanDate': None, 'createPlanDateLong': None,
     'createdByErpDb': False, 'createdById': 158372, 'dataNotEqualEGRUL': False, 'dataSetNotInTime': False,
     'deleted': False, 'directDurationDays': None, 'disapprove': False, 'district': 'Кемеровская область',
     'districtId': 1035320000000001, 'durationDays': 10, 'durationHours': None, 'erknmActViolationIds': [],
     'erknmResultKindDecisionIds': [], 'erpId': '42220041000101607846', 'events': [], 'federalLaw': '248',
     'federalLawId': 3, 'fullFieldViolationKnm': False, 'hasViolations': False, 'id': 11679971, 'inn': '4245001792',
     'inspectorFullName': [], 'isFromSmev': False, 'isHasApproveDocs': False, 'isHasCollaboratingOrganization': False,
     'isHasRequirements': False, 'isHasViolationTerm': False, 'isPm': False, 'kind': 'Выездная проверка',
     'knmAnnulled': False, 'knmRejected': False, 'knmType': 'Внеплановое КНМ', 'knmTypeId': 5, 'legalBasisDocName': [],
     'links': [], 'mspCategory': ['Не является субъектом МСП'], 'noPunishment': False, 'notifyLate': False,
     'objectsKind': [], 'objectsSubKind': [], 'objectsType': [], 'ogrn': '1024202004177', 'oldKnm': None,
     'oldPlan': None, 'orderDone': False,
     'organizationName': 'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ "СОЦИАЛЬНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ НЕСОВЕРШЕННОЛЕТНИХ ЮРГИНСКОГО МУНИЦИПАЛЬНОГО ОКРУГА "СОЛНЫШКО"',
     'organizationsInn': ['4245001792'], 'organizationsName': [
        'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ "СОЦИАЛЬНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ НЕСОВЕРШЕННОЛЕТНИХ ЮРГИНСКОГО МУНИЦИПАЛЬНОГО ОКРУГА "СОЛНЫШКО"'],
     'organizationsOgrn': ['1024202004177'], 'planId': None,
     'prosecutorOrganization': 'Прокуратура Кемеровской области', 'prosecutorOrganizationId': 2282,
     'publishedStatus': 'UNPUBLISHED', 'reasons': [], 'reasonsList': [], 'recEmptyOrLate': False,
     'regDateEgrul': '31.01.2022', 'regDateEgrulEn': '2022-01-31', 'regLate': False, 'regTypes': [], 'requirements': 0,
     'requirementsList': [], 'resolved': False, 'resultEmpty': True, 'resultEmptyOrLate': False,
     'resultInfoTypeCodes': [], 'resultViolationKnm': False, 'riskCategory': [], 'riskCategoryAndDangerClass': [],
     'sezRegistryExists': False, 'signed': False, 'smevInfoType': None, 'smevMessageType': None, 'smevReceivedAt': None,
     'smevReceivedAtEn': None, 'smevReceivedAtMonth': None, 'smevReceivedAtYear': None, 'spvRegistryExists': False,
     'startDate': '02.02.2022', 'startDateEn': '2022-02-02', 'status': 'В процессе заполнения', 'statusEgrul': 'Найден',
     'statusId': 11, 'stopDate': '15.02.2022', 'stopDateEn': '2022-02-15', 'subjectTypeId': 0,
     'supervisionType': 'Федеральный государственный санитарно-эпидемиологический контроль (надзор)',
     'supervisionTypeId': 4, 'torRegistryExists': False, 'updatePlanDate': None, 'updatePlanDateLong': None,
     'version': 'ERKNM', 'violationLawsuitTypeCodes': [], 'violationTypeCodes': [], 'year': 2022},
    {'actCreateDate': None, 'actCreateDateEn': None, 'addresses': [], 'admLevelId': 50001, 'appealed': False,
     'approveDocOrderDate': '02.02.2022', 'approveDocOrderNum': '76-ВН', 'approveDocRequestDate': None,
     'approveDocRequestNum': None, 'approveDocs': [], 'approveRequired': False, 'approved': None, 'approvedErknm': None,
     'chlistCount': 0, 'chlistFilledCount': 0, 'chlistFillingIndicationTypeId': [], 'collaboratingOrganizations': [],
     'collaboratingOrganizationsIds': [], 'comment': None,
     'controllingOrganization': 'Управление Роспотребнадзора по Кемеровской области ',
     'controllingOrganizationId': 10001011723, 'createPlanDate': None, 'createPlanDateLong': None,
     'createdByErpDb': False, 'createdById': 158372, 'dataNotEqualEGRUL': False, 'dataSetNotInTime': False,
     'deleted': False, 'directDurationDays': None, 'disapprove': False, 'district': 'Кемеровская область',
     'districtId': 1035320000000001, 'durationDays': 10, 'durationHours': None, 'erknmActViolationIds': [],
     'erknmResultKindDecisionIds': [], 'erpId': '42220041000101607846', 'events': [], 'federalLaw': '248',
     'federalLawId': 3, 'fullFieldViolationKnm': False, 'hasViolations': False, 'id': 11679971, 'inn': '4245001792',
     'inspectorFullName': [], 'isFromSmev': False, 'isHasApproveDocs': False, 'isHasCollaboratingOrganization': False,
     'isHasRequirements': False, 'isHasViolationTerm': False, 'isPm': False, 'kind': 'Выездная проверка',
     'knmAnnulled': False, 'knmRejected': False, 'knmType': 'Внеплановое КНМ', 'knmTypeId': 5, 'legalBasisDocName': [],
     'links': [], 'mspCategory': ['Не является субъектом МСП'], 'noPunishment': False, 'notifyLate': False,
     'objectsKind': [], 'objectsSubKind': [], 'objectsType': [], 'ogrn': '1024202004177', 'oldKnm': None,
     'oldPlan': None, 'orderDone': False,
     'organizationName': 'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ "СОЦИАЛЬНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ НЕСОВЕРШЕННОЛЕТНИХ ЮРГИНСКОГО МУНИЦИПАЛЬНОГО ОКРУГА "СОЛНЫШКО"',
     'organizationsInn': ['4245001792'], 'organizationsName': [
        'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ "СОЦИАЛЬНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ НЕСОВЕРШЕННОЛЕТНИХ ЮРГИНСКОГО МУНИЦИПАЛЬНОГО ОКРУГА "СОЛНЫШКО"'],
     'organizationsOgrn': ['1024202004177'], 'planId': None,
     'prosecutorOrganization': 'Прокуратура Кемеровской области', 'prosecutorOrganizationId': 2282,
     'publishedStatus': 'UNPUBLISHED', 'reasons': [], 'reasonsList': [], 'recEmptyOrLate': False,
     'regDateEgrul': '31.01.2022', 'regDateEgrulEn': '2022-01-31', 'regLate': False, 'regTypes': [], 'requirements': 0,
     'requirementsList': [], 'resolved': False, 'resultEmpty': True, 'resultEmptyOrLate': False,
     'resultInfoTypeCodes': [], 'resultViolationKnm': False, 'riskCategory': [], 'riskCategoryAndDangerClass': [],
     'sezRegistryExists': False, 'signed': False, 'smevInfoType': None, 'smevMessageType': None, 'smevReceivedAt': None,
     'smevReceivedAtEn': None, 'smevReceivedAtMonth': None, 'smevReceivedAtYear': None, 'spvRegistryExists': False,
     'startDate': '02.02.2022', 'startDateEn': '2022-02-02', 'status': 'В процессе заполнения', 'statusEgrul': 'Найден',
     'statusId': 11, 'stopDate': '15.02.2022', 'stopDateEn': '2022-02-15', 'subjectTypeId': 0,
     'supervisionType': 'Федеральный государственный санитарно-эпидемиологический контроль (надзор)',
     'supervisionTypeId': 4, 'torRegistryExists': False, 'updatePlanDate': None, 'updatePlanDateLong': None,
     'version': 'ERKNM', 'violationLawsuitTypeCodes': [], 'violationTypeCodes': [], 'year': 2022},

]

def list_to_json():
    with open('Exception_knm.json', 'w') as file:
        json.dump(list, file)


def request_constructor(targets: list, table: str = 'erknm', **params):
    target_text = ''
    if target_text:
        print('yt gecnjq')
    for target in targets:
        if target_text:
            target_text += f', {target}'
        else:
            target_text += target
    params_text = ''
    for db_column, value in params.items():

        if isinstance(value, type(list)):
            values_text = ''
            for v in value:
                if values_text:
                    values_text += f", '{v}'"
                else:
                    values_text += f"'{v}'"
            if params_text:
                params_text += f" AND {db_column} IN ({values_text})"
            else:
                params_text += f" WHERE {db_column} IN ({values_text})"
        else:
            if params_text:
                params_text += f" AND {db_column}='{value}'"
            else:
                params_text += f" WHERE {db_column}='{value}'"
    if params_text:
        text = f"""SELECT {target_text} FROM {table}{params_text};"""
    else:
        text = f"""SELECT {target_text} FROM {table};"""
    return text


if __name__ == '__main__':

    request = request_constructor(['id', 'kind'], year='2023', kind=['kind_1', 'kind_2'])
    print(request)



