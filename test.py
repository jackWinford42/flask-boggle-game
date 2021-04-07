from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Initial variable declaration for set up"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Ensure various HTML and data are present on homepage"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('n_plays'))
            self.assertIn(b'<p>Current High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """check if a valid word works as expected when guessed"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "O", "G", "G", "G"], 
                                ["B", "O", "G", "G", "G"], 
                                ["B", "O", "G", "G", "G"], 
                                ["B", "O", "G", "G", "G"], 
                                ["B", "O", "G", "G", "G"]]

        response = self.client.get('/check-word?word=bog')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """check if a real word is in the dictionary but not the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=abalienation')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """check if a non-word returns not-word"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=reqwtyifdaskgjzvcxvmmbfgjlkvbnerfdvb')
        self.assertEqual(response.json['result'], 'not-word')