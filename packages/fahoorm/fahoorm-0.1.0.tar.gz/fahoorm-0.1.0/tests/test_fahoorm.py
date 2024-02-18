import unittest
from fahoorm import Entity, Session

class TestFahoORM(unittest.TestCase):
    def test_entity(self):
        entity = Entity()
        self.assertIsNone(entity.id)
        entity.id = 1
        self.assertEqual(entity.id, 1)

    def test_session(self):
        session = Session("sqlite:///:memory:")
        self.assertIsNotNone(session.connection)
        self.assertIsNotNone(session.cursor)
        session.close()
