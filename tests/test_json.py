import datetime

from decimal import Decimal
from unittest import TestCase

from induction import Induction, jsonify

app = Induction(__name__)


class JSONTests(TestCase):
    def test_json(self):
        self.assertEqual(jsonify("foo"), '"foo"')
        self.assertEqual(len(jsonify(datetime.datetime.now())), 25)
        self.assertEqual(len(jsonify(datetime.date.today())), 12)
        self.assertEqual(jsonify(Decimal("0.12")), '"0.12"')
        self.assertEqual(jsonify(datetime.timedelta(seconds=12)), '"12.0"')
