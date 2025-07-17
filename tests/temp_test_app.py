import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', email='testuser@example.com', role='admin')
            user.set_password('testpass')  # Asegúrate que User tenga este método
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)  # Ajusta según texto en dashboard.html

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_users_list(self):
        self.login()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)


if __name__ == '__main__':
    unittest.main()
