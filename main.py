import csv
import re


# Логика чтения адресной книги в формате CSV в список
def open_data():
    with open("files/phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


# Основная логика преобразования исходных данных в требуемый вид
def reformat_data(contacts_list):
    pattern = r'(\+7|8)+\s*\(?(\d{3})\)?\s*\-?(\d{3})\-?(\d{2})\-?(\d{2})\s*\(?(\w*\.?)\s*(\d*)\)?'
    substitute = r'+7(\2)\3-\4-\5 \6\7'
    reformat_list = []
    for contact in contacts_list:
        reformat_contact = []
        name = ','.join(contact[:3])
        reformat_name = re.findall(r'(\w+)', name)
        while len(reformat_name) < 3:
            reformat_name.append('')
        reformat_contact += reformat_name
        reformat_contact.append(contact[3])
        reformat_contact.append(contact[4])
        phone_reg = re.compile(pattern)
        reformat_phone = (phone_reg.sub(substitute, contact[5])).rstrip()
        reformat_contact.append(reformat_phone)
        reformat_contact.append(contact[6])
        reformat_list.append(reformat_contact)
    return reformat_list


# Логика объединения контактов с одинаковыми фамилией и именем
def unite_repeat(reformat_list):
    reformat_dict_unite = {}
    for contact in reformat_list:
        if f'{contact[0]} {contact[1]}' in reformat_dict_unite:
            contact_exist = reformat_dict_unite[contact[0] + ' ' + contact[1]]
            for i in range(len(contact_exist)):
                if contact[i] != '':
                    contact_exist[i] = contact[i]
        else:
            reformat_dict_unite[contact[0] + ' ' + contact[1]] = contact
    return list(reformat_dict_unite.values())


# Логика записи полученных данных в файл CSV
def write_reformat_data(contacts):
    with open("files/phonebook.csv", "w", newline='', encoding='utf-8') as f:
        data_writer = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        data_writer.writerows(contacts)


contacts_raw = open_data()
contacts_reformat = reformat_data(contacts_raw)
contacts_unite = unite_repeat(contacts_reformat)
write_reformat_data(contacts_unite)
