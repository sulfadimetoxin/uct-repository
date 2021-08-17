import json
import csv
import requests
from datetime import datetime
import taxonomies_mapping
import sample_db

counter = -1
schema = {}
get_date_modified = ''
contr_list = []


with open('students_data.csv', 'r') as r:
    reader = csv.reader(r, delimiter=',', quotechar='"')
    for row in reader:
        if row == EOFError:
            break
        if counter == -1:
            date_issued = row.index('akademicky_rok')
            date_modified = row.index('kdy')
            control_number = row.index('did')
            language = row.index('jazyk')
            title = row.index('nazev_v_jazyce_prace')
            title_cs = row.index('nazev_cs')
            title_en = row.index('nazev_en')
            abstract = row.index('anotace')
            abstract_cs = row.index('anotace_cs')
            abstract_en = row.index('anotace_en')
            creator_surname = row.index('diplom_prijmeni')
            creator_name = row.index('diplom_jmeno')
            creator_titul_pred = row.index('diplom_tituly_pred')
            creator_titul_za = row.index('diplom_tituly_za')
            contributor = row.index('osoby')
            provider = row.index('ustav')
            accessRight = row.index('neverejna')
            resource = row.index('druh_id')
            field = row.index('obor')
            counter = 1
            continue
        if counter != 16:

            try:
                get_date_modified = sample_db.session.query(sample_db.ModDate.date_modified). \
                    filter_by(control_number=row[control_number]).one()
            except sample_db.sqlalchemy.orm.exc.NoResultFound:
                get_date_modified = 'None'

            if get_date_modified[0] == row[date_modified] or get_date_modified[0] > row[date_modified]:
                counter = counter + 1
                continue

            schema['$schema'] = 'https://repozitar.vscht.cz/schemas/uct_repository_theses/uct-repository-theses-v1.0.0.json'
            schema['keywords'] = [{"cs": "test1"}, {"cs": "test2"}, {"cs": "test3"}]
            schema['control_number'] = row[control_number]

            if row[title] != '' and row[title_en] != '':
                schema['title'] = [{'cs': (row[title_cs] if row[language] == 'en' else row[title])},
                                   {'en': row[title_en]}]
            elif row[title_en] == '':
                schema['title'] = [{'cs': (row[title_cs] if row[language] == 'en' else row[title])}]
            else:
                schema['title'] = [{'cs': 'No data'}]

            if row[abstract] != '' and row[abstract_en] != '':
                schema['abstract'] = {'cs': (row[abstract_cs] if row[language] == 'en' else row[abstract]),
                                      'en': row[abstract_en]}
            elif row[abstract] != '' and row[abstract_en] == '':
                schema['abstract'] = {'cs': row[abstract_cs] if row[language] == 'en' else row[abstract]}
            else:
                pass

            schema['language'] = taxonomies_mapping.language[row[language]]
            schema['resourceType'] = taxonomies_mapping.resourceType[row[resource]]
            schema['creator'] = [{'name': (row[creator_surname] + " " + row[creator_name]
                                           + ((" " + row[creator_titul_pred]) if row[creator_titul_pred] != '' else "")
                                           + ((" " + row[creator_titul_za]) if row[creator_titul_za] != '' else ""))}]

            if row[contributor] != '':
                contr_dict = row[contributor]
                contr_dict = contr_dict[1:]
                contr_dict = contr_dict[:-1]
                temp_list = contr_dict.split(', \n ')
                contr = ''
                for i in range(len(temp_list)):
                    contr_dict = json.loads(temp_list[i])
                    contr = contr + "{'name': '" + str(contr_dict['prijmeni']) + " " + str(contr_dict['jmeno']) \
                            + ((" " + str(contr_dict['tituly_pred'])) if contr_dict['tituly_pred'] != '' else "") \
                            + ((" " + str(contr_dict['tituly_za']) + "'") if contr_dict['tituly_za'] != '' else "'") \
                            + ", 'role': '" + str(taxonomies_mapping.contributorType[contr_dict['typ_id']]) + "'}, "
                contr = contr[:-2]
                contr = eval(contr)
                if len(contr) > 2:
                    for i in range(len(contr)):
                        contr_list.append(contr[i])
                    schema['contributor'] = contr_list
                else:
                    schema['contributor'] = [contr]
            else:
                schema['contributor'] = [{'name': 'No data',
                                          'role': 'https://127.0.0.1:8080/api/2.0/taxonomies/contributor-type/supervisor'}]

            if row[provider] != '':
                prov_dict = row[provider]
                prov_dict = prov_dict[1:]
                prov_dict = prov_dict[:-1]
                prov_dict = json.loads(prov_dict)
                schema['provider'] = taxonomies_mapping.provider[prov_dict['nazev_cs']]
            else:
                schema['provider'] = 'https://127.0.0.1:8080/api/2.0/taxonomies/institutions/vscht'

            schema['accessRights'] = taxonomies_mapping.accessRights[row[accessRight]]
            schema['dateIssued'] = row[date_issued]
            schema['defended'] = True
            schema['dateDefended'] = '2021-06-06'
            schema['degreeGrantor'] = 'https://127.0.0.1:8080/api/2.0/taxonomies/institutions/vscht'

            if get_date_modified == 'None':
                temp = requests.post("https://127.0.0.1:8080/api/theses/", headers={"Content-Type": "application/json"},
                                     json=schema, verify=False)
                if temp:
                    sample_db.session.add(sample_db.ModDate(
                        control_number=schema['control_number'],
                        date_modified=row[date_modified]))
                    sample_db.session.commit()
                else:
                    print(temp.content)
            else:
                del schema['control_number']
                temp = requests.put("https://127.0.0.1:8080/api/theses/{}".format(row[control_number]),
                                    headers={"Content-Type": "application/json"}, json=schema, verify=False)
                sample_db.session.query(sample_db.ModDate). \
                    filter_by(control_number=row[control_number]).update({"date_modified": row[date_modified]})
                sample_db.session.commit()

            counter = counter + 1


# with open('/home/denys/PycharmProjects/uct-repository/tests/sample_data/36521.json', encoding='utf-8') as f: obsah
# = f.read() data = json.loads(obsah) temp = requests.post("https://127.0.0.1:8080/api/theses/",
# headers={"Content-Type": "application/json"}, json=data, verify=False)

# pprint(temp.content)


