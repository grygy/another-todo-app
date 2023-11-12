import unittest
from unittest.mock import Mock
from uuid import UUID

from crud.base_crud import BaseCRUD, HasId
from db.repository import IRepository


class TestBaseCRUD(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=IRepository)
        self.base_crud = BaseCRUD(self.mock_repository)

    def test_get(self):
        mock_id = UUID("123e4567-e89b-12d3-a456-426614174001")
        mock_item = Mock(spec=HasId)
        self.mock_repository.get_by_id.return_value = mock_item

        result = self.base_crud.get(mock_id)

        self.assertEqual(result, mock_item)
        self.mock_repository.get_by_id.assert_called_once_with(mock_id)

    def test_get_all(self):
        mock_item_list = [Mock(spec=HasId) for _ in range(3)]
        self.mock_repository.get_all.return_value = mock_item_list

        result = self.base_crud.get_all()

        self.assertEqual(result, mock_item_list)
        self.mock_repository.get_all.assert_called_once()

    def test_create(self):
        mock_item_without_id = Mock()
        mock_created_item = Mock(spec=HasId)
        self.mock_repository.create.return_value = mock_created_item

        result = self.base_crud.create(mock_item_without_id)

        self.assertEqual(result, mock_created_item)
        self.mock_repository.create.assert_called_once_with(mock_item_without_id)

    def test_update(self):
        mock_item_with_id = Mock(spec=HasId)
        self.mock_repository.update.return_value = mock_item_with_id

        result = self.base_crud.update(mock_item_with_id)

        self.assertEqual(result, mock_item_with_id)
        self.mock_repository.update.assert_called_once_with(mock_item_with_id)

    def test_delete(self):
        mock_id = UUID("123e4567-e89b-12d3-a456-426614174001")

        self.base_crud.delete(mock_id)

        self.mock_repository.delete.assert_called_once_with(mock_id)


if __name__ == '__main__':
    unittest.main()
