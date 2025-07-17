import unittest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('password'),
                role='user'
            )
            db.session.add(user)
            db.session.commit()


    def login(self):
        return self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class AuthTestCase(BaseTestCase):
    def test_login(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_logout(self):
        self.login()
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dashboard(self):
        self.login()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_users_list(self):
        self.login()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Users', response.data)

    #def test_register_route_should_exist(self):
    #    response = self.client.get('/register')
    #    self.assertEqual(response.status_code, 200)
    #    self.assertIn(b'Register', response.data)


if __name__ == '__main__':
    unittest.main()

