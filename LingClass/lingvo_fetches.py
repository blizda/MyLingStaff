import string
import xml
from re import findall
import re

from nltk.corpus import stopwords

import nltk
import pymorphy2
import math

from LingClass.parsing.MyXMLParser import MyXMLParser


class lingvo_fetches:

    def __init__(self, file_name):
        self.file_name = file_name
        self.__ent_val = []
        self.__redab_val = []
        self.__analit_val = []
        self.__glagol_val = []
        self.__substat_val =[]
        self.__adjekt_val = []
        self.__mestoim_val = []
        self.__autosem_val = []
        self.__lex_razn_val = []
        self.__kol_per_lex_in_t_val = []
        self.__neznam_val = []
        self.__imen_lex_val = []
        self.__text_mass = []
        self.__list_of_lems = []
        self.__surpris_val = []
        self.__way_to_lems_dic = 'lems.txt'
        try:
            if (file_name.endswith('.xml')):
                parser = xml.sax.make_parser()
                hand = MyXMLParser()
                parser.setContentHandler(hand)
                parser.parse(file_name)
                self.__text_mass = hand.retData()
            else:
                f = open(file_name, 'r')
                self.__text_mass = f.readlines()
                f.close()
        except FileNotFoundError:
            print('can not read %s, please check name' % (file_name))

    def set_way_to_dic(self, val):
        if (type(val) == str):
            self.__way_to_lems_dic = val

    @property
    def get_surprisal(self):
        if len(self.__surpris_val) > 0:
            return self.__surpris_val
        else:
            return self.__surprisal()

    @property
    def get_redab(self):
        if len(self.__redab_val) > 0:
            return self.__redab_val
        else:
            return self.__readabilyte()

    @property
    def get_ent(self):
        if len(self.__ent_val) > 0:
            return self.__ent_val
        else:
            return self.__entrop()

    @property
    def get_anality(self):
        if len(self.__analit_val) > 0:
            return self.__analit_val
        else:
            self.__all_fetches()
            return self.__analit_val

    @property
    def get_glagolity(self):
        if len(self.__glagol_val) > 0:
            return self.__glagol_val
        else:
            self.__all_fetches()
            return self.__analit_val

    @property
    def get_substativ(self):
        if len(self.__substat_val) > 0:
            return self.__substat_val
        else:
            self.__all_fetches()
            return self.__substat_val

    @property
    def get_adjekt(self):
        if len(self.__adjekt_val) > 0:
            return self.__adjekt_val
        else:
            self.__all_fetches()
            return self.__adjekt_val

    @property
    def get_mestoim(self):
        if len(self.__mestoim_val) > 0:
            return self.__mestoim_val
        else:
            self.__all_fetches()
            return self.__mestoim_val

    @property
    def get_autosem(self):
        if len(self.__autosem_val) > 0:
            return self.__autosem_val
        else:
            self.__all_fetches()
            return self.__autosem_val

    @property
    def get_lex_raz(self):
        if len(self.__lex_razn_val) > 0:
            return self.__lex_razn_val
        else:
            self.__all_fetches()
            return self.__lex_razn_val

    @property
    def get_kol_per_lex(self):
        if len(self.__kol_per_lex_in_t_val) > 0:
            return self.__kol_per_lex_in_t_val
        else:
            self.__all_fetches()
            return self.__kol_per_lex_in_t_val

    @property
    def get_neznam(self):
        if len(self.__neznam_val) > 0:
            return self.__neznam_val
        else:
            self.__all_fetches()
            return self.__neznam_val

    @property
    def get_imen_lex(self):
        if len(self.__imen_lex_val) > 0:
            return self.__imen_lex_val
        else:
            self.__all_fetches()
            return self.__imen_lex_val

    @staticmethod
    def __tokens(line):
        tokens_ent = nltk.word_tokenize(line.lower())
        stop_words = stopwords.words('russian')
        stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', "и"])
        tokens_ent = [i for i in tokens_ent if ( i not in stop_words )]
        tokens_ent = [i for i in tokens_ent if ( i not in string.punctuation )]
        tokens_ent = [i.replace("«", "").replace("»", "").replace("…","").replace("\'\'","").replace("\?","\.")
                          .replace("!","\.").replace("!\?","\.").replace("?\!","\.").replace(",","").replace("-","")
                          .replace("``", "").replace("—", "").replace("*", "") for i in tokens_ent]
        tokens_ent = [re.sub("(\d+)", "", i) for i in tokens_ent]
        tokens_ent = [i for i in tokens_ent if i]
        return tokens_ent

    def __link_lems_dic(self, way_to_lems_dic):
        file = open(way_to_lems_dic, 'r')
        try:
            lems_dic = file.readlines()
            file.close()
        except FileNotFoundError:
            print('can not read %s' %(way_to_lems_dic))
        else:
            for line in lems_dic:
                lems = self.__tokens(line)
                self.__list_of_lems.extend(lems)

    def __surprisal(self):
        morph = pymorphy2.MorphAnalyzer()
        list_of_words_in_text = {}
        bigram_list = {}
        self.__surpris_val.clear()
        words_in_text = 0
        for line in self.__text_mass:
            str_of_text = self.__tokens(line)
            if str_of_text:
                words_in_text += len(str_of_text)
                for i in range(len(str_of_text)):
                    str_of_text[i] = morph.parse(str_of_text[i])[0].normal_form
                    if i > 0:
                        if (str_of_text[i - 1] + ' ' + str_of_text[i]) in bigram_list:
                            bigram_list[str_of_text[i - 1] + ' ' + str_of_text[i]] = bigram_list.get(str_of_text[i - 1] + ' ' + str_of_text[i]) + 1
                        else:
                            bigram_list[str_of_text[i - 1] + ' ' + str_of_text[i]] = 1
                    if str_of_text[i] in list_of_words_in_text:
                        list_of_words_in_text[str_of_text[i]] = list_of_words_in_text.get(str_of_text[i]) + 1
                    else:
                        list_of_words_in_text[str_of_text[i]] = 1
            else:
                surpr = 0
                for key in bigram_list.keys():
                    sovm = bigram_list[key]/ words_in_text
                    cont_tok = key.split()
                    context = list_of_words_in_text[cont_tok[0]] / words_in_text
                    surpr += math.log2(1 / (sovm / context))
                self.__surpris_val.append(surpr / words_in_text)
                words_in_text = 0
                list_of_words_in_text.clear()
                bigram_list.clear()
        return self.__surpris_val

    def __entrop(self):
        morph = pymorphy2.MorphAnalyzer()
        list_of_words_in_text = {}
        words_in_text = 0
        self.__ent_val.clear()
        total_words_in_text = []
        pit_mass = []
        kol_text = 0
        for line in self.__text_mass:
            str_of_text = self.__tokens(line)
            print(str_of_text)
            if str_of_text:
                kol_text += 1
                words_in_text += len(str_of_text)
                for i in range(len(str_of_text)):
                    str_of_text[i] = morph.parse(str_of_text[i])[0].normal_form
                    if str_of_text[i] in list_of_words_in_text:
                        list_of_words_in_text[str_of_text[i]] = list_of_words_in_text.get(str_of_text[i]) + 1
                    else:
                        list_of_words_in_text[str_of_text[i]] = 1

            else:
                entropy = 0
                for key in list_of_words_in_text.keys():
                    p_i = list_of_words_in_text[key] / words_in_text
                    pit_mass.append(p_i)
                    entropy += list_of_words_in_text[key] * (p_i * math.log(p_i))
                self.__ent_val.append((-1) * entropy)
                total_words_in_text.append(words_in_text)
                words_in_text = 0
                list_of_words_in_text.clear()
        return self.__ent_val

    def __readabilyte(self):
        words_in_text = 0
        col_slog = 0
        num_sentans = 0
        num_sentans_total = []
        words_in_text_total = []
        col_slog_total = []
        glas = ['а','у','о','ы','и','э','я','ю','ё','е']
        self.__link_lems_dic(self.__way_to_lems_dic)
        for line in self.__text_mass:
            str_of_text = self.__tokens(line)
            num_sentans += len(findall('\.|\?!|\?|! ', line))
            for r in range (len(glas)):
                col_slog += line.count(glas[r])
            if str_of_text:
                words_in_text += len(str_of_text)
            else:
                readab = (((words_in_text - num_sentans) / num_sentans) * 0.39) + (col_slog / (words_in_text - num_sentans)) - 15.59
                if readab < 0:
                    readab = (-1) / readab
                self.__redab_val.append(readab)
                num_sentans_total.append(num_sentans)
                words_in_text_total.append(words_in_text - num_sentans)
                col_slog_total.append(col_slog)
                words_in_text = 0
                num_sentans = 0
                col_slog = 0
        return self.__redab_val

    def __all_fetches(self):
        self.__link_lems_dic(self.__way_to_lems_dic)
        words_in_text = 0
        kol_lex = 0
        morph = pymorphy2.MorphAnalyzer()
        chasti_rechi = {'NOUN': 0, 'ADJF': 0, 'COMP': 0, 'VERB': 0, 'INFN': 0, 'PRTF': 0, 'PRTS': 0, 'GRND': 0,
                        'NUMR': 0, 'ADVB': 0, 'NPRO': 0, 'PRED': 0, 'PREP': 0, 'CONJ': 0, 'ADJS': 0, 'PRCL': 0, 'INTJ': 0}
        list_of_words_in_text = {}
        kol_per_lex = 0
        for line in self.__text_mass:
            str_of_text = self.__tokens(line)
            if str_of_text:
                words_in_text += len(str_of_text)
                for i in range(len(str_of_text)):
                    str_of_text[i] = morph.parse(str_of_text[i])[0].normal_form
                    p = morph.parse(str_of_text[i])[0]
                    razb = p.tag.POS
                    if razb in chasti_rechi:
                        chasti_rechi[razb] = chasti_rechi.get(razb) + 1
                    else:
                        chasti_rechi[razb] = 1
                    if str_of_text[i] in list_of_words_in_text:
                        list_of_words_in_text[str_of_text[i]] = list_of_words_in_text.get(str_of_text[i]) + 1
                    else:
                        list_of_words_in_text[str_of_text[i]] = 1
            else:
                self.__analit_val.append((chasti_rechi.get('PREP') + chasti_rechi.get('CONJ')
                                          + chasti_rechi.get('PRCL')) / words_in_text)
                self.__glagol_val.append((chasti_rechi.get('VERB') + chasti_rechi.get('INFN') + chasti_rechi.get('PRTF') +
                                          chasti_rechi.get('PRTS') + chasti_rechi.get('GRND')) / words_in_text)
                self.__substat_val.append((chasti_rechi.get('NOUN')) / words_in_text)
                self.__adjekt_val.append((chasti_rechi.get('ADJF') + chasti_rechi.get('ADJS')) / words_in_text)
                self.__mestoim_val.append(chasti_rechi.get('NPRO') / words_in_text)
                self.__autosem_val.append((words_in_text - (chasti_rechi.get('PREP') + chasti_rechi.get('CONJ') + chasti_rechi.get('PRCL'))
                                           - chasti_rechi.get('NPRO')) / words_in_text)
                for key in list_of_words_in_text.keys():
                    if (self.__list_of_lems.count(key) == 1):
                        kol_per_lex += 1
                    kol_lex += 1
                self.__lex_razn_val.append(kol_lex / words_in_text)
                self.__kol_per_lex_in_t_val.append(kol_per_lex / words_in_text)
                self.__neznam_val.append((chasti_rechi.get('PREP') + chasti_rechi.get('CONJ') +
                                          chasti_rechi.get('PRCL') + chasti_rechi.get('NPRO')) / words_in_text)
                self.__imen_lex_val.append((chasti_rechi.get('NOUN') + chasti_rechi.get('ADJF')
                                            + chasti_rechi.get('ADJS')) / words_in_text)
                kol_per_lex = 0
                kol_lex = 0
                words_in_text = 0
                list_of_words_in_text.clear()
                chasti_rechi.clear()
                chasti_rechi = {'NOUN': 0, 'ADJF': 0, 'COMP': 0, 'VERB': 0, 'INFN': 0, 'PRTF': 0, 'PRTS': 0, 'GRND': 0, 'NUMR': 0,
                                'ADVB': 0, 'NPRO': 0, 'PRED': 0, 'PREP': 0, 'CONJ': 0, 'ADJS': 0, 'PRCL': 0, 'INTJ': 0}