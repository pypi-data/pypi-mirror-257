# -*- coding: utf-8 -*-
import unittest

from a3py.simplified import dynamic
from tests.test_simplified.dynamic import Animal, Dog, Cat, Bird, Eagle


class T(unittest.TestCase):

    def test__find_all_subclasses__success(self):
        animal_class_list = dynamic.find_all_subclasses('tests.test_simplified.dynamic', Animal)
        self.assertTrue(Animal not in animal_class_list)
        self.assertTrue(Dog in animal_class_list)
        self.assertTrue(Cat in animal_class_list)
        self.assertTrue(Bird in animal_class_list)
        self.assertTrue(Eagle in animal_class_list)

        bird_class_list = dynamic.find_all_subclasses('tests.test_simplified.dynamic', Bird)
        self.assertTrue(Animal not in bird_class_list)
        self.assertTrue(Dog not in bird_class_list)
        self.assertTrue(Cat not in bird_class_list)
        self.assertTrue(Bird not in bird_class_list)
        self.assertTrue(Eagle in bird_class_list)

    def test__import_string(self):
        klass = dynamic.import_string("tests.test_simplified.dynamic.Animal")
        self.assertTrue(klass is Animal)

        with self.assertRaises(ImportError):
            dynamic.import_string("test_dynamic")

        with self.assertRaises(ImportError):
            dynamic.import_string("tests.test_simplified.dynamic.WangZai")
