import unittest
import uuid
from typing import List
from unittest.mock import patch
from uuid import UUID

from crud.base import BaseCRUD


def get_mock_uuid():
    return uuid.UUID("bd65600d-8669-4903-8a14-af88203add38")


class MockItemCreate:
    def __init__(self, data: str):
        self.data = data


class MockItem:
    def __init__(self, data: str, mock_id: UUID = None):
        self.data = data
        self.id = mock_id


class TestBaseCRUD(unittest.TestCase):

    def setUp(self) -> None:
        self.db: List[MockItem] = []
        self.crud = BaseCRUD[MockItem, MockItemCreate](self.db)

    @patch('uuid.uuid4')
    def test_create(self, mock_uuid4):
        mock_uuid4.return_value = get_mock_uuid()

        item = MockItemCreate(data="test data")
        created_item = self.crud.create(item)

        self.assertIn(created_item, self.db)
        self.assertIsNotNone(created_item.id)
        self.assertEqual(created_item.id, get_mock_uuid())

    def test_get(self):
        item = MockItem(data="test data")
        self.db.append(item)

        retrieved_item = self.crud.get(item.id)

        self.assertEqual(retrieved_item, item)

    def test_get_all(self):
        self.db: List[MockItem] = [MockItem(data=f"data_{i}") for i in range(3)]
        self.crud = BaseCRUD[MockItem, MockItemCreate](self.db)
        all_items = self.crud.get_all()

        self.assertEqual(all_items, self.db)

    def test_update(self):
        item = MockItem(data="test data")
        self.db.append(item)

        updated_item = MockItem(data="updated data", mock_id=item.id)
        self.crud.update(updated_item)

        self.assertIn(updated_item, self.db)

    def test_delete(self):
        item = MockItem(data="test data")
        self.db.append(item)

        self.crud.delete(item.id)

        self.assertNotIn(item, self.db)


if __name__ == '__main__':
    unittest.main()
