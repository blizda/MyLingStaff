import re
import chardet

class my_tokens:

    __text_mass = ''
    __clear_tokens = []
    __punct_mass = ['.', ',', '?', '!', '"', '-', ':', '(', ')', '*', ';', '…', '«', '»', '[', ']', '{', '}', '<', '>']
    __end_of_text = ['.', '?', '!', '*', '"', ';', ':', '…']
    __occur_of_ent_mass = []

    def __init__(self, file_name):
        self.file_name = file_name
        try:
            f = open(file_name, 'rb').read()
            z = chardet.detect(f)
            self.__text_mass = self.__text_mass + f.decode(z['encoding'])
        except FileNotFoundError:
            print('can not read %s, please check name' % (file_name))
    def __init__(self, string):
        self.__text_mass = string

    def __is_url(self, line):
        if re.match('(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?', line) is not None:
            return True
        else:
            return False

    def __is_fraction(self, line):
        if re.match('\d+(\.|,)\d+', line) is not None:
            return True
        else:
            return False

    def __is_initials(self, line):
        if re.match('\[A-ZА-Я]{1}\.[A-ZА-Я]{1}', line) is not None:
            return True
        else:
            return False

    def __is_name(self, line):
        if re.match('(([А-Я]){1}([а-я])+-{1})+((([а-я])+|(([А-Я]){1}([а-я])*))-{1}){0,3}(([А-Я]){1}([а-я])+)', line) is not None:
            return True
        else:
            return False

    def __really_retard_pars(self, line):
        self.__occur_of_ent_mass.clear()
        num_of_entry = 0
        for el in line:
            if el in self.__punct_mass:
                self.__occur_of_ent_mass.append(num_of_entry)
            num_of_entry += 1
        if self.__occur_of_ent_mass:
            return True
        else:
            return False


    def __pars_punct(self, line):
        tokens = []
        oc_of_ent_pr = 0
        for el in self.__occur_of_ent_mass:
            oc_of_ent = el
            if oc_of_ent == 0:
                tokens.append(line[:el + 1])
                oc_of_ent_pr = oc_of_ent + 1
                continue
            elif oc_of_ent == len(line) - 1:
                tokens.append(line[oc_of_ent_pr:oc_of_ent])
                tokens.append(line[oc_of_ent:])
                break
            else:
                tokens.append(line[oc_of_ent_pr:oc_of_ent])
                tokens.append(line[oc_of_ent:oc_of_ent + 1])
            oc_of_ent_pr = oc_of_ent + 1
        else:
            tokens.append(line[oc_of_ent_pr:])
        return tokens

    def __pars_end_of(self, i, tok):
        if (len(tok) == i + 2):
            return False
        elif (tok[i + 2] == '"') and (tok[i] == '"'):
            return False
        elif re.match('([А-Я]+[а-я]*)|([A-Z]+[a-z]*)', tok[i + 1]) or (tok[i + 1] == '–'):
            return True
        else:
            return False

    def tokens(self):
        tokens = re.split('\s+', self.__text_mass)
        self.__clear_tokens.clear()
        for line in tokens:
            if self.__is_url(line):
                self.__clear_tokens.append(line)
            elif self.__is_fraction(line):
                self.__clear_tokens.append(line)
            elif self.__is_initials(line):
                self.__clear_tokens.append(line)
            elif self.__is_name(line):
                self.__clear_tokens.append(line)
            elif self.__really_retard_pars(line):
                self.__clear_tokens.extend(self.__pars_punct(line))
            else:
                self.__clear_tokens.append(line)
        self.__clear_tokens = [value for value in self.__clear_tokens if value]
        return self.__clear_tokens

    def sigmentation(self, tok):
        priv_end = 0
        count_of_pr = 1
        dict_of_pr = {}
        i = 0
        for el in tok:
            if el in self.__end_of_text:
                if i == len(tok) - 1:
                    dict_of_pr[count_of_pr] = tok[priv_end + 1:]
                    priv_end = i
                    count_of_pr += 1
                elif priv_end == 0:
                    dict_of_pr[count_of_pr] = tok[:i + 1]
                    priv_end = i
                    count_of_pr += 1
                elif self.__pars_end_of(i, tok):
                    dict_of_pr[count_of_pr] = tok[priv_end + 1:i + 1]
                    priv_end = i
                    count_of_pr += 1
            i += 1
        return dict_of_pr