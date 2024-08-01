import csv
import re

with open("input_phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    headers = next(rows)
    contacts_list = list(rows)

pattern_fio = re.compile('(^\w+)[\s,?](\w+)[\s,?](?:(\w+)(,{0,3})|,{0,2})')
pattern_phone = re.compile('\+?([7-8])[\s\(]?[\(]?(\d{3})[\s\)-]?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s?)')
pattern_phone_dob = re.compile('\+?([7-8])[\s\(]?[\(]?(\d{3})[\s\)-]?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s?)[(доб.\s]+(\d+)\)?')
sub_fio = r'\1,\2,\3,'
sub_phone = r'+7(\2)\3-\4-\5'
sub_phone_dob = r'+7(\2)\3-\4-\5 доб.\7'
contacts_list_out = []


def merge_dicts(contact_list, dir_str):
    flag = False
    for el in contact_list:
        if el['lastname'] == dir_str['lastname'] and el['firstname'] == dir_str['firstname']:
            for key, value in dir_str.items():
                if value == '':
                    continue
                else:
                    el.update({key: value})
                    flag = True
    return flag


for row in contacts_list:
    str_row = ','.join(row)
    result_fio = pattern_fio.sub(sub_fio, str_row)
    search_phone = pattern_phone.search(result_fio)
    if search_phone is None:
        dict_row = dict(zip(headers, result_fio.split(',')))
        if merge_dicts(contacts_list_out, dict_row):
            continue
        else:
            contacts_list_out.append(dict_row)
    elif search_phone.group(6) == ' ':
        result_fio_ph = pattern_phone_dob.sub(sub_phone_dob, result_fio)
        dict_row = dict(zip(headers, result_fio_ph.split(',')))
        if merge_dicts(contacts_list_out, dict_row):
            continue
        else:
            contacts_list_out.append(dict_row)
    else:
        result_fio_ph = pattern_phone.sub(sub_phone, result_fio)
        dict_row = dict(zip(headers, result_fio_ph.split(',')))
        if merge_dicts(contacts_list_out, dict_row):
            continue
        else:
            contacts_list_out.append(dict_row)

with open('output_phonebook_raw.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for data in contacts_list_out:
        writer.writerow(data)
