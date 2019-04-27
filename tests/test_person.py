# -*- coding: utf-8 -*- 
import unittest
from .context import src
from unittest import TestCase


class PersonTest(unittest.TestCase):
    def setUp(self):
        src.Person._registry = []
        self.person = src.Person( first_name="ken", last_name= "odoh",  company_name="query", address="query", city="query", province="query", postal="query", phone1="876876587658", phone2="6786784536436", email="query@gmail.com", web="query.com", default=True )


    def test_email_is_valid(self):
        email = "kenneth.odoh@gmail.com"
        self.assertTrue(self.person.is_Valid_Email( email ))


    def test_email_is_not_valid(self):
        email = "kenneth.odohgmail.com"
        self.assertFalse(self.person.is_Valid_Email( email ))


    def test_input_length_is_valid(self):
        self.assertTrue(self.person.is_Length_Valid( ))

    def test_input_length_is_not_valid(self):
        self.person.dictObj = {"first_name": "ken", "last_name": "odoh", "company_name":"query", "address":"query", "city":"query", "province":"query", "postal":"query", "phone":"876876587658", "phone2":"0"*269, "email":"query@gmail.com", "web":"query.com"}
        self.assertFalse(self.person.is_Length_Valid( ))


    def test_input_is_Mandatory(self):
        self.person.dictObj = {"first_name": "ken", "last_name": "odoh", "company_name":"query", "address":"query", "city":"query", "province":"query", "postal":"query", "phone":"876876587658", "phone2":"6786784536436", "email":"query@gmail.com", "web":"query.com"}

        self.assertTrue(self.person.is_Mandatory( ))


    def test_input_is_not_Mandatory(self):
        self.person.dictObj = {"first_name": "", "last_name": "", "company_name":"query", "address":"query", "city":"query", "province":"query", "postal":"query", "phone":"876876587658", "phone2":"6786784536436", "email":"query@gmail.com", "web":"query.com"}

        self.assertFalse(self.person.is_Mandatory( ))


    def test_name_is_valid (self):
        name = "Sahar"
        self.assertTrue(self.person.is_Valid_Name(name))

        name = "Rodriguez", 
        self.assertTrue(self.person.is_Valid_Name(name))

        name = "Van Gogh"
        self.assertTrue(self.person.is_Valid_Name(name))

        name = "Smith-Jones"
        self.assertTrue(self.person.is_Valid_Name(name))


    def test_name_is_not_valid (self):
        name = "--"
        self.assertFalse(self.person.is_Valid_Name(name))

        name = "Müller", 
        self.assertFalse(self.person.is_Valid_Name(name))

        name = "Harper7"
        self.assertFalse(self.person.is_Valid_Name(name))

    """
    def tearDown (self):
        del src.Person._registry
    """

if __name__ == '__main__':
    unittest.main(verbosity=2)
