from sql import Database



d = Database()
# ter_upr_name = knm['controllingOrganization']
# controllingOrganizationID = knm['controllingOrganizationID']
# ter_upr_name_id = d.insert_terr_upr_with_return_id(name=ter_upr_name, controllingOrganizationID=controllingOrganizationID)

def create_knm_in_knms(knm):

    # for number, (key, value) in enumerate(knm.items()):
    #     print(key, value)
    terr_upr_id = d.create_terr_upr_returned_id(knm['controllingOrganization'], knm['controllingOrganizationId'], knm['district'])
    try:
        last_inspect_date = knm['reasonsList']['o']['date']
    except:
        last_inspect_date = '1990-01-01'

    desicion_date = knm['approveDocOrderDate']
    if desicion_date is None:
        desicion_date = '1900-01-01'

    date_end = knm['stopDateEn']
    if date_end is None:
        date_end = '1900-01-01'


    comment = knm['comment']
    comment = formattig_str(comment)

    insp_id = d.create_inspection_knd_returned_id(plan_id=knm['planId'],
                                                  knm_id=knm['id'],
                                                  kind=knm['kind'],
                                                  profilactic=knm['isPm'],
                                                  deleted=knm['deleted'],
                                                  date_start=knm['startDateEn'],
                                                  date_end=date_end,
                                                  desicion_number=knm['approveDocOrderNum'],
                                                  desicion_date=desicion_date,
                                                  last_inspection_date_end=last_inspect_date,
                                                  mspCategory=formattig_str(knm['mspCategory'][0]),
                                                  number=knm['erpId'],
                                                  status=formattig_str(knm['status']),
                                                  comment=comment,
                                                  year=knm['year'],
                                                  terr_upr_id=terr_upr_id)
    address = formattig_str(knm['addresses'][-1])
    # print(address)
    subject_id = d.create_subject_with_returned_id(

        name=formattig_str(knm['organizationName']),
        address=address,
        inn=knm['inn'],
        ogrn=knm['ogrn']
    )
    for address, risk in zip(knm['addresses'], knm['riskCategory']):
        address = formattig_str(address)
        object_id = d.create_object_with_returned_id(
            subject=subject_id,
            kind=formattig_str(knm['objectsKind'][0]),
            address=formattig_str(address),
            risk=formattig_str(risk)
        )
        d.insert_m_to_m_object_inspection(inspection_id=insp_id, object_id=object_id)


def insert_in_database(list_knm: list):
    for knm in list_knm:
        print(knm)
        id = int(knm['erpId'])
        kind = knm['kind']
        type = knm['knmType']
        status = knm['status']
        year = int(knm['year'])
        start_date = knm['startDateEn']
        stop_date = knm['stopDateEn']
        if stop_date is None:
            stop_date = '1900-01-01'
        inn = int(knm['inn'])
        ogrn = int(knm['ogrn'])
        risk = knm['riskCategory'][0]
        # if risk is None:
        #     risk = 'NULL'
        object_kind = knm['objectsKind'][0]
        # if object_kind is None:
        #     object_kind = 'NULL'
        controll_organ = knm['controllingOrganization']
        data = str(knm).replace('"', '').replace('None', "'None'").replace('False', "'False'").replace('True', "'True'").replace("'", '"').replace('\\n', '').replace('\\t', '').replace('\\p', '')
        try:
            Database().create_json_formate_knm_in_raw_knm(id, kind, type, status, year, start_date, stop_date, inn, ogrn, risk, object_kind, controll_organ, data)
        except Exception as ex:
            print(ex)
            print(knm)

def formattig_str(text):
    text = str(text).replace("'", "").replace('"', '')
    return text


def create_tables_for_knms(knm):
    code = ''
    for key, value in knm.items():


        if isinstance(value, list):
            types = 'TEXT'
            code += f'{key} {types}, '
            continue

        elif value is None or isinstance(value, str):
            types = 'VARCHAR(255)'
            code += f'{key} {types}, '
            continue



        elif value is True or value is False:
            print('bool')
            types = 'BOOL'
            code += f'{key} {types}, '
            continue

        elif isinstance(value, int):

            types = 'INT'
            code += f'{key} {types}, '
            continue

    print(str(code).strip())


if __name__ == '__main__':
    pass
    # create_knm_in_knms(knm)

