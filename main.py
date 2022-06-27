import re
from pprint import pprint
import csv

class Contact():
    def __init__(self, lastname, firstname, surname, organization='', position='', phone='', email=''):
        self.lastname = lastname
        self.firstname = firstname
        self.surname = surname
        self.organization = organization
        self.position = position
        self.phone = phone
        self.email = email
    def __str__(self):
        return self.lastname + '|' + self.firstname + '|' + self.surname + '|' + self.organization + '|' + self.position + '|' + self.phone + '|' + self.email

def creat_new_contact(man_text, class_list):
    list1 = re.findall('^(([А-Я][а-я]+)[ ]+([А-Я][а-я]+)[ ]?([А-Я][а-я]+вич|[А-Я][а-я]+вна)?[ ])', man_text, re.U)
    lastname = list1[0][1]
    firstname = list1[0][2]
    surname = list1[0][3]

    man_text2 = re.sub('^(([А-Я][а-я]+)[ ]+([А-Я][а-я]+)[ ]?([А-Я][а-я]+вич|[А-Я][а-я]+вна)?[ ]+)', '', man_text)
    list2 = re.findall('^([А-Я][А-Яа-я]+)?', man_text2, re.U)
    if len(list2) > 0: organization = list2[0]
    else: organization = ''

    man_text3 = re.sub('^([А-Я][А-Яа-я]+)?[ ]+', '', man_text2)
    list3 = re.findall('\S+@\S+', man_text3, re.U)
    if len(list3) > 0:
        email = list3[0]
    else:
        email = ''

    man_text4 = re.sub('\S+@\S+', '', man_text3)
    list4 = re.findall('^(\D+[ ])', man_text4, re.U)
    if len(list4) > 0:
        position = list4[0]
    else:
        position = ''

    man_text5 = re.sub('^(\D+[ ])', '', man_text4)
    list5 = re.findall('\d', man_text5, re.U)
    if len(list5) == 10:
        phone = '+7(' + ''.join(list5[:3]) + ')' + ''.join(list5[3:6]) + '-' + ''.join(list5[6:8]) + '-' + ''.join(list5[8:])
    elif len(list5) == 11:
        phone = '+7(' + ''.join(list5[1:4]) + ')' + ''.join(list5[4:7]) + '-' + ''.join(list5[7:9]) + '-' + ''.join(list5[9:])
    elif len(list5) > 11:
        phone = '+7(' + ''.join(list5[1:4]) + ')' + ''.join(list5[4:7]) + '-' + ''.join(list5[7:9]) + '-' + ''.join(list5[9:11]) + ' доб.' + ''.join(list5[11:])
    elif len(list5) > 0: phone = ''.join(list5)
    else: phone = ''

    if len(class_list) > 0:
        IND_0 = True
        for contact in class_list:
            ind1 = (lastname == contact.lastname)
            ind2_1 = (contact.firstname == '')
            ind2_2 = (firstname == contact.firstname) or (firstname == '')
            ind3_1 = (contact.surname == '')
            ind3_2 = (surname == contact.surname) or (surname == '')

            if (ind1 + ind2_1 + ind2_2 + ind3_1 + ind3_2) > 2: IND_0 = False
        if IND_0:
            class_list += [Contact(lastname, firstname, surname, organization, position, phone, email)]
        else:
            if (contact.firstname == '') and (firstname != ''): contact.firstname = firstname
            if (contact.surname == '') and (surname != ''): contact.surname = surname
            if (contact.organization == '') and (organization != ''): contact.organization = organization
            if (contact.position == '') and (position != ''): contact.position = position
            if (contact.phone == '') and (phone != ''): contact.phone = phone
            if (contact.email == '') and (email != ''): contact.email = email
    else:
        class_list += [Contact(lastname, firstname, surname, organization, position, phone, email)]


if __name__ == '__main__':
    contacts_list = []
    class_list = []
    contacts_list2 = []

    # TODO 1: Чтение файла
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # TODO 2: выполнение пунктов 1-3 ДЗ

    for i_1 in range(1, len(contacts_list)):
        man_text = ' '.join(contacts_list[i_1])
        creat_new_contact(man_text, class_list)

    for contact in class_list:
        contacts_list2 += [[contact.lastname, contact.firstname, contact.surname, contact.organization, contact.position, contact.phone, contact.email]]

    # TODO 3: сохраните получившиеся данные в другой файл
    with open("phonebook2.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list2)