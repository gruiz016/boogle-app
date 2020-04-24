from unittest import TestCase
from app import app, check_word, request
from flask import session, jsonify
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_index(self):
        '''Test the homepage, displays the board'''
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<table class="board">', html)
            self.assertEqual(session['times-played'], 1)

    def test_check_word(self):
        '''Test if the word is on the board'''
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"]]
            res = client.get('/check-word?word=cat')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'ok')
