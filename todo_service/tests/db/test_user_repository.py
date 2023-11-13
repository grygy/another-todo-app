import unittest
from uuid import uuid4

from sqlalchemy import create_engine

from db.connection import Database
from db.user_repository import UserRepository
from models.user import UserInDb


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')

        self.database = Database.get_instance(self.engine)
        self.database.create_all()

        self.user_repository = UserRepository(self.database)

    def tearDown(self):
        self.database.drop_all()

    def test_create_user(self):
        user = UserInDb(id=uuid4(), username="testuser", hashed_password="testpassword")

        created_user = self.user_repository.create(user)

        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, user.username)
        self.assertEqual(created_user.hashed_password, user.hashed_password)

    def test_get_all_users(self):
        user1 = UserInDb(id=uuid4(), username="testuser1", hashed_password="testpassword1")
        user2 = UserInDb(id=uuid4(), username="testuser2", hashed_password="testpassword2")
        self.user_repository.create(user1)
        self.user_repository.create(user2)

        users = self.user_repository.get_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, user1.username)
        self.assertEqual(users[0].hashed_password, user1.hashed_password)
        self.assertEqual(users[1].username, user2.username)
        self.assertEqual(users[1].hashed_password, user2.hashed_password)

    def test_get_user_by_id(self):
        user = UserInDb(id=uuid4(), username="testuser", hashed_password="testpassword")
        self.user_repository.create(user)

        retrieved_user = self.user_repository.get_by_id(user.id)

        self.assertEqual(retrieved_user.username, user.username)
        self.assertEqual(retrieved_user.hashed_password, user.hashed_password)

    def test_get_user_by_username(self):
        user = UserInDb(id=uuid4(), username="testuser", hashed_password="testpassword")
        self.user_repository.create(user)

        retrieved_user = self.user_repository.get_by_username(user.username)

        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_user.hashed_password, user.hashed_password)

    def test_update_user(self):
        user = UserInDb(id=uuid4(), username="testuser", hashed_password="testpassword")
        self.user_repository.create(user)

        user.username = "updateduser"
        user.hashed_password = "updatedpassword"
        updated_user = self.user_repository.update(user)

        self.assertEqual(updated_user.username, user.username)
        self.assertEqual(updated_user.hashed_password, user.hashed_password)

    def test_delete_user_by_id(self):
        user = UserInDb(id=uuid4(), username="testuser", hashed_password="testpassword")
        self.user_repository.create(user)

        self.user_repository.delete(user.id)

        should_be_none = self.user_repository.get_by_id(user.id)

        self.assertIsNone(should_be_none)


if __name__ == '__main__':
    unittest.main()
