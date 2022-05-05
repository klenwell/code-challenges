"""
A quick introduction to Python Data Classes.

Based on https://realpython.com/python-data-classes
"""
from dataclasses import dataclass
from typing import Any
import time
import unittest


@dataclass
class User:
    id: str = ''

    def __post_init__(self):
        if not self.id:
            self.id = self.autogenerate_id()

    def autogenerate_id(self):
        return str(time.time()).replace('.', '-')


@dataclass
class FeatureFlag:
    key: str
    owner: Any
    status: str = 'disabled'
    owner_id: str = ''
    owner_type: str = ''

    def __post_init__(self):
        self.owner_id = self.owner.id
        self.owner_type = self.owner.__class__.__name__

    def is_enabled(self):
        return self.status == 'enabled'


class UserTest(unittest.TestCase):
    def test_expects_instance(self):
        user = User()
        self.assertIsInstance(user, User)

    def test_expects_autogenerated_id(self):
        user = User()
        self.assertIsInstance(user.id, str)
        self.assertGreater(len(user.id), 12)


class FeatureFlagTest(unittest.TestCase):
    def test_expects_instance(self):
        # Arrange
        owner = User()
        flag_key = 'test'
        ff = FeatureFlag(key=flag_key, owner=owner)

        self.assertIsInstance(ff, FeatureFlag)
        self.assertEqual(ff.key, flag_key)
        self.assertEqual(ff.owner_id, owner.id)
        self.assertEqual(ff.owner_type, 'User')
        self.assertEqual(ff.is_enabled(), False)

    def test_expects_types_to_be_hints_only(self):
        ff = FeatureFlag(key=123, owner=User())
        self.assertNotIsInstance(ff.key, str)
        self.assertIsInstance(ff.key, int)

    def test_expects_to_be_enabled(self):
        ff = FeatureFlag(key='test', owner=User(), status='enabled')
        self.assertEqual(ff.is_enabled(), True)


if __name__ == '__main__':
    unittest.main()
