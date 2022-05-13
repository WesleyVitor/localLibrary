from calendar import week
from django.test import TestCase

from catalog.forms import RenewBookForm

from datetime import timedelta, date

class RenewBookFormTest(TestCase):

    def test_renewal_date_label(self):
        form = RenewBookForm()
        label = form.fields['renewal_date'].label
        self.assertTrue(label == None or label == 'renewal date') 
    
    def test_renewal_date_help_text(self):
        form = RenewBookForm()
        help_text = form.fields['renewal_date'].help_text
        self.assertEqual(help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renewal_date_in_past(self):
        past_date = date.today() - timedelta(days=1)
        form = RenewBookForm(data={'renewal_date':past_date})
        self.assertFalse(form.is_valid())
    
    def test_renewal_date_in_today(self):
        today = date.today()
        form = RenewBookForm(data={'renewal_date':today})
        self.assertTrue(form.is_valid())
    
    def test_renewal_date_in_limit_date(self):
        limit_date = date.today() + timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date':limit_date})
        self.assertTrue(form.is_valid())
    
    def test_renewal_date_in_overlimit(self):
        overlimit_date = date.today() + timedelta(weeks=4) + timedelta(days=1)
        form = RenewBookForm(data={'renewal_date':overlimit_date})
        self.assertFalse(form.is_valid())