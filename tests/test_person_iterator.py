# -*- coding: utf-8 -*- 
import unittest
from .context import src
from unittest import TestCase
import pandas as pd
import os


class PersonIterator(unittest.TestCase):

    def setUp(self):

        src.Person._registry = []
        filename = os.path.abspath("tests/data/simple_test_file.csv")
        self.df = pd.read_csv(filename)
        self.personIter = src.PersonIterator(filename)

    def test_has_relatives(self):
        src.Person._registry = []
        first_name, last_name = "Xavier", "William-Scott"
        lst = self.personIter.getRelatives(first_name, last_name)

        self.assertTrue(len( set(lst)) > 0)

    def test_has_no_relatives(self):
        src.Person._registry = []
        first_name, last_name = "XXXXXXXXXCVBCB", "XXXXXXXCVBVBDFGDX"
        lst = self.personIter.getRelatives(first_name, last_name)
        self.assertTrue(len(lst) == 0)


    def test_lastnames_matches_file_content(self):
        lnameSet = set()
        for index, row in self.df.iterrows():
            # split the lastname and insert the data
            lnameArr = row["last_name"].split("-")
            for lname in lnameArr:
                lnameSet.add(lname)

        tokenizedlistofnames = set(self.personIter.getSetOfLastName(  ))
        self.assertTrue(len(lnameSet ) == len(lnameSet & tokenizedlistofnames))




if __name__ == '__main__':
    unittest.main(verbosity=2)
