# -*- coding: utf-8 -*- 
import pandas as pd
from Trie import Trie
from collections import defaultdict
import re
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Person(object):
    """
    This is the blue print for a person.
    """

    _registry = []
    _maxlength = 256

    # first_name,last_name,company_name,address,city,province,postal,phone1,phone2,email,web

    def __init__(self, first_name, last_name, company_name, address, city, province, postal, phone1, phone2, email, web, max=1000, default=True):
        """
        Initialize a person and validate the input
        @input: string
        first_name, last_name, company_name, address, city, province, postal, phone1, phone2, email, web
        @return None
        """

        self.dictObj = {"first_name": first_name, "last_name": last_name, "company_name": company_name, "address": address,
                        "city": city, "province": province, "postal": postal, "phone1": phone1, "phone2": phone2, "email": email, "web": web}

        if self.is_Length_Valid() and self.is_Mandatory() and self.is_Valid_Email(email) and self.is_Valid_Name(first_name) and self.is_Valid_Name(last_name):
            if len(self._registry) < max:
                if default:
                    self._registry.append(self)
                self.first_name = first_name
                self.last_name = last_name
                self.company_name = company_name
                self.address = address
                self.city = city
                self.province = province
                self.postal = postal
                self.phone1 = phone1
                self.phone2 = phone2
                self.email = email
                self.web = web

            else:
                raise StopIteration
        else:
            logger.info('Invalid Data Input')

    @classmethod
    def fromconstructor(cls, first_name, last_name,  company_name="query", address="query", city="query", province="query", postal="query", phone1="876876587658", phone2="6786784536436", email="query@gmail.com", web="query.com", default=False):
        """
        Provide default argumment to pass validation to the original constructor
        @input: string
        first_name, last_name, company_name, address, city, province, postal, phone1, phone2, email, web
        @return constructor
        """
        return cls(first_name, last_name, company_name, address, city, province, postal, phone1, phone2, email, web, default=default)

    def is_Length_Valid(self):
        """
        The data input of acceptable length.
        @input: None
        @return boolean
        """

        for key, value in self.dictObj.items():
            if len(value) > self._maxlength:
                logger.info(
                    'Invalid Length of Input: {}  -  {}'.format(key, value))
                return False
        return True

    def is_Mandatory(self):
        """
        The data input is mandatory.
        @input: None
        @return boolean
        """
        keylist = ["first_name", "last_name", "email"]

        for key, value in self.dictObj.items():
            if key in keylist:
                if len(value) == 0:
                    logger.info(
                        'Is Input Mandatory: {}  -  {}'.format(key, value))
                    return False
        return True

    def is_Valid_Email(self, addressToVerify):
        """
        checks if the email is valid
        @input: string 
        addressToVerify
        @return boolean
        """
        match = re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

        if match == None:
            logger.info('Bad Email Syntax: {} '.format(addressToVerify))
            return False
        return True

    def is_Valid_Name(self, name):
        """
        Checks if the name is valid.
        @input: string 
        name
        @return boolean
        """

        # strip and check for emptiness
        # check for only spaces
        # check for only hyphen
        # check for at least one character with remaining hyphens and spaces
        def containsLetter(s):
            letter_flag = False
            for i in s:
                if i.isalpha():
                    letter_flag = True
            return letter_flag

        def containsPermittedLetter(s):
            letter_flag = False
            permlist = [" ", "-"]
            for i in s:
                if not i.isalpha() and i not in permlist:
                    letter_flag = True
            return letter_flag

        nlen = len(name)
        no_space = 0
        no_hyphen = 0

        for c in name:
            if c == " ":
                no_space = no_space + 1
            if c == "-":
                no_hyphen = no_hyphen + 1

        if no_space == nlen:

            logger.info('Name is only spaces: {} '.format(name))
            return False

        elif no_hyphen == nlen:
            logger.info('Name is only hyphens: {} '.format(name))
            return False

        elif containsPermittedLetter(name):
            logger.info('Name is only permitted characters: {} '.format(name))
            return False

        elif not containsLetter(name):
            logger.info('Name does not have alphabets: {} '.format(name))
            return False

        return True


class PersonIterator(object):
    """
    This is the blue print for an iterator of a person class.
    """

    _list_of_persons = None

    def __init__(self, filename):
        """
        The constructor accepts the file as input.
        @input: string 
        filename
        @return None
        """
        self.loadFromFile(filename)
        self.tree = Trie()
        self.store = defaultdict(list)
        self.build_Tree( )
        Person._registry = []

    def loadFromFile(self, filename):
        """
        load the file
        @input: string 
        filename
        @return None
        """
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            #first_name, last_name = row["first_name"], row["last_name"]

            first_name, last_name, company_name, address, city, province, postal, phone1, phone2, email, web = row["first_name"], row["last_name"], row[
                "company_name"], row["address"], row["city"], row["province"], row["postal"], row["phone1"], row["phone2"], row["email"], row["web"]

            p = Person(first_name, last_name, company_name, address,
                       city, province, postal, phone1, phone2, email, web)
        self._list_of_persons = Person._registry

    def getSetOfLastName(self):
        """
        build a unique list of surnames
        @input: None
        @return List
        """
        lnameSet = set()
        for p in self._list_of_persons:
            # split the lastname and insert the data
            lnameArr = p.last_name.split("-")
            for lname in lnameArr:
                lnameSet.add(lname)
        return list(lnameSet)

    def one_hot_encoding_vectors(self):
        """
        convert names to one-hot encoded vectors
        @input: None
        @return List
        """
        totalVector = []
        totalLastNameSet = self.getSetOfLastName()
        # use a trie data structure to get candidate output and do a anding operation to make it better

        for person in self._list_of_persons:
            curVec = [0] * len(totalLastNameSet)
            lnameArr = person.last_name.split("-")
            for lname in lnameArr:
                if lname in totalLastNameSet:
                    ind = totalLastNameSet.index(lname)
                    curVec[ind] = 1

            curVec = ''.join(str(w) for w in curVec)
            totalVector.append(curVec)

            # Add to help retrieval
            self.store[curVec].append(person)

        return totalVector

    def build_Tree(self):
        """
        build the tree
        @input: None
        @return None
        """
        # use a trie data structure to get candidate output

        list_of_vectors = self.one_hot_encoding_vectors()
        for cur in list_of_vectors:
            self.tree.insert(cur)

    def search_Tree(self, person):
        """
        search the Tree for nearest neighbours
        @input: Person 
        person
        @return list
        """
        totalLastNameSet = self.getSetOfLastName()
        curVec = [0] * len(totalLastNameSet)
        lnameArr = person.last_name.split("-")
        for lname in lnameArr:
            if lname in totalLastNameSet:
                ind = totalLastNameSet.index(lname)
                curVec[ind] = 1
        lastnameEncoding = ''.join(str(w) for w in curVec)

        ind = lastnameEncoding.find("1")
        if ind == -1:
            return []
        prefix = lastnameEncoding[:ind+1]
        return self.tree.get_all_with_prefix(prefix)

    def getRelatives(self, first_name, last_name):
        """
        get the list of relative related to the person 
        @input: string 
        first_name, last_name
        @return list
        """
        output = []
        person = Person.fromconstructor(first_name, last_name)

        prefixes = self.search_Tree(person)
        for curVec in prefixes:
            output.extend(self.store[curVec])

        return list(set([obj for obj in output if obj.first_name != person.first_name and obj.last_name != person.last_name])) #exclude yourself from your relatives

    def printRelatives(self, first_name, last_name, filename="output/output.txt"):
        """
        print the list of relatives
        @input: string 
        filename first_name, last_name, filename
        @return None
        """
        lst = self.getRelatives(first_name, last_name)
        nlist = [elem.first_name + " " + elem.last_name for elem in lst]

        print ("{} {}: {}".format(first_name, last_name,  ",".join(nlist)))

        with open(filename, 'a') as file:  # Use file to refer to the file object
            file.write("{} {}: {}".format(
                first_name, last_name,  ",".join(nlist)))
