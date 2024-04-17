#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''this will test the FileStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""

        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()
        key = "{}.{}".format(type(cls.base).__name__, cls.base.id)
        FileStorage._FileStorage__objects[key] = cls.base
        cls.user = User()
        key = "{}.{}".format(type(cls.user).__name__, cls.user.id)
        FileStorage._FileStorage__objects[key] = cls.user
        cls.state = State()
        key = "{}.{}".format(type(cls.state).__name__, cls.state.id)
        FileStorage._FileStorage__objects[key] = cls.state
        cls.city = City()
        key = "{}.{}".format(type(cls.city).__name__, cls.city.id)
        FileStorage._FileStorage__objects[key] = cls.city
        cls.amenity = Amenity()
        key = "{}.{}".format(type(cls.amenity).__name__, cls.amenity.id)
        FileStorage._FileStorage__objects[key] = cls.amenity
        cls.place = Place()
        key = "{}.{}".format(type(cls.place).__name__, cls.place.id)
        FileStorage._FileStorage__objects[key] = cls.place
        cls.review = Review()
        key = "{}.{}".format(type(cls.review).__name__, cls.review.id)
        FileStorage._FileStorage__objects[key] = cls.review

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.base
        del cls.user
        del cls.state
        del cls.city
        del cls.place
        del cls.amenity
        del cls.review

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_attr(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_hasattr(self):
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertTrue(hasattr(FileStorage, "new"))
        self.assertTrue(hasattr(FileStorage, "reload"))
        self.assertTrue(hasattr(FileStorage, "delete"))

    def test_docstr(self):
        self.assertIsNotNone(FileStorage.__doc__)
        self.assertIsNotNone(FileStorage.all.__doc__)
        self.assertIsNotNone(FileStorage.new.__doc__)
        self.assertIsNotNone(FileStorage.reload.__doc__)
        self.assertIsNotNone(FileStorage.delete.__doc__)

    def test_all(self):
        """tests if all works in File Storage"""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, FileStorage._FileStorage__objects)

    def test_new(self):
        """test when new is created"""
        BModel = BaseModel()
        self.storage.new(BModel)
        storag = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + BModel.id, storag.keys())
        self.assertIn(self.base, storag.values())

    def test_reload_filestorage(self):
        """
        tests reload
        """
        BModel = BaseModel()
        with open("file.json", "w", encoding="utf-8") as f:
            key = "{}.{}".format(type(BModel).__name__, BModel.id)
            json.dump({key: BModel.to_dict()}, f)
        self.storage.reload()
        storag = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + BModel.id, storag)

    def test_delete(self):
        BModel = BaseModel()
        key = "{}.{}".format(type(BModel).__name__, BModel.id)
        FileStorage._FileStorage__objects[key] = BModel
        self.storage.delete(BModel)
        self.assertNotIn(BModel, FileStorage._FileStorage__objects)

    def test_save(self):
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            saves = f.read()
            self.assertIn("BaseModel." + self.base.id, saves)
            self.assertIn("User." + self.user.id, saves)
            self.assertIn("Place." + self.place.id, saves)
            self.assertIn("State." + self.state.id, saves)
            self.assertIn("City." + self.city.id, saves)
            self.assertIn("Review." + self.review.id, saves)
            self.assertIn("Amenity." + self.amenity.id, saves)


if __name__ == "__main__":
    unittest.main()
