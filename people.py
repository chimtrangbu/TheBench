#!/usr/bin/env python3


class Person():
    def __init__(self, line):
        infor = line.split(',')
        self.first_name = infor[0]
        self.last_name = infor[1]
        self.username = infor[2]
        self.age = int(infor[3])
        self.gender = infor[4]
        self.city = infor[5]

    def get_value(self, field):
        if field == 'first_name':
            return self.first_name
        elif field == 'last_name':
            return self.last_name
        elif field == 'username':
            return self.username
        elif field == 'age':
            return self.age
        elif field == 'gender':
            return self.gender
        elif field == 'city':
            return self.city

    def select(self, fields):
        # return fields' values should be printed out
        outputs = []
        fields_list = fields.split(', ')
        for field in fields_list:
            outputs.append(str(self.get_value(field)))
        return ', '.join(outputs)

    def verify(self, condition):
        # verify a line to be returned
        left = condition['left']
        if 'first_letter' in left:
            value = self.get_value(left[13:])[0]
        else:
            value = self.get_value(left)
        try:
            right = int(condition['right'])
        except ValueError:
            right = condition['right']
        op = condition['op']
        if op == '<':
            return value < right
        elif op == '>':
            return value > right
        elif op == '=':
            return value == right
        else:
            return value != right

    def all_conds(self, list_conds):
        # all conditions indicated must be verified for a line to be returned
        for cond in list_conds:
            if not self.verify(cond):
                return False
        return True

    def one_cond(self, list_conds):
        # at least 1 of th conditions indicated must be verified to be returned
        for cond in list_conds:
            if self.verify(cond):
                return True
        return False


class ListPeople():
    def __init__(self, data):
        self.people_list = []
        for line in data:
            self.people_list.append(Person(line[:-1]))

    def query(self, query_dict):
        queried = []
        if 'where_and' in query_dict.keys():
            for person in self.people_list:
                if person.all_conds(query_dict['where_and']):
                    queried.append(person)
        elif 'where_or' in query_dict.keys():
            for person in self.people_list:
                if person.one_cond(query_dict['where_or']):
                    queried.append(person)
        else:
            queried = self.people_list
        if 'order' in query_dict.keys():
            queried.sort(key=lambda e: e.get_value(query_dict['order']))
        if 'select' in query_dict.keys():
            fields = query_dict['select']
        else:
            fields = 'first_name, last_name, username, age, gender, city'
        result = []
        for person in queried:
            result.append(person.select(fields))
        return '\n'.join(result)
