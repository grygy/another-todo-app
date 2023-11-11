import unittest
import uuid
from typing import List
from unittest.mock import patch

from crud.base_crud import BaseCRUD
from models.todo import TodoCreate, Todo


def get_mock_uuid():
    return uuid.UUID("bd65600d-8669-4903-8a14-af88203add38")


class TestBaseCRUD(unittest.TestCase):

    def setUp(self) -> None:
        self.db: List[Todo] = []
        self.crud = BaseCRUD[Todo, TodoCreate](self.db)

    @patch('uuid.uuid4')
    def test_create(self, mock_uuid4):
        mock_uuid4.return_value = get_mock_uuid()

        item = TodoCreate(title="test title", description="test description")
        created_item = self.crud.create(item)

        self.assertIn(created_item, self.db)
        self.assertIsNotNone(created_item.id)
        self.assertEqual(created_item.id, get_mock_uuid())

    def test_get(self):
        item = Todo(title="test title", description="test description", id=get_mock_uuid())
        self.db.append(item)

        retrieved_item = self.crud.get(item.id)

        self.assertEqual(retrieved_item, item)

    def test_get_all(self):
        self.db: List[Todo] = [Todo(title=f"title_{i}", description=f"description_{i}", id=uuid.uuid4()) for i in
                               range(3)]
        self.crud = BaseCRUD[Todo, TodoCreate](self.db)
        all_items = self.crud.get_all()

        self.assertEqual(all_items, self.db)

    def test_update(self):
        item = Todo(title="test title", description="test description", id=get_mock_uuid())
        self.db.append(item)

        updated_item = Todo(title="updated title", description="updated description", id=get_mock_uuid())
        self.crud.update(updated_item)

        self.assertIn(updated_item, self.db)

    def test_delete(self):
        item = Todo(title="test title", description="test description", id=get_mock_uuid())
        self.db.append(item)

        self.crud.delete(item.id)

        self.assertNotIn(item, self.db)


if __name__ == '__main__':
    unittest.main()
