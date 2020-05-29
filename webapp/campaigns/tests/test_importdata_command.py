from django.core.management import call_command
from django.test import TestCase

from ..models import Impression, Click, Conversion


class ImportDataTest(TestCase):
    def test_duplicate_data_logs(self):
        with self.assertLogs(level='WARN') as logs:
            call_command('importdata',
                         '--base_path=campaigns/tests/test_csvs/',
                         '--num_periods=1')

        duplicate_count = 0
        for line in logs.output:
            if 'duplicate' in line:
                duplicate_count += 1

        self.assertEqual(duplicate_count, 9)

    def test_load_impressions(self):
        with self.assertLogs(level='WARN') as logs:
            call_command('importdata',
                         '--base_path=campaigns/tests/test_csvs/',
                         '--num_periods=1')

        impressions = [
            Impression(period=1, banner_id=1, campaign_id=100),
            Impression(period=1, banner_id=1, campaign_id=200),
            Impression(period=1, banner_id=2, campaign_id=100),
            Impression(period=1, banner_id=2, campaign_id=200),
            Impression(period=1, banner_id=3, campaign_id=300),
            Impression(period=1, banner_id=3, campaign_id=400),
            Impression(period=1, banner_id=4, campaign_id=100),
            Impression(period=1, banner_id=4, campaign_id=200),
            Impression(period=1, banner_id=4, campaign_id=300),
            Impression(period=1, banner_id=4, campaign_id=400),
        ]

        loaded_impressions = Impression.objects.all()
        self.assertEqual(len(loaded_impressions), 10)

        for impression in impressions:
            # Have to do this because PKs are unknown.
            filtered_count = len(Impression.objects.filter(
                period=impression.period,
                banner_id=impression.banner_id,
                campaign_id=impression.campaign_id,
            ))
            self.assertEqual(filtered_count, 1)

    def test_load_clicks(self):
        with self.assertLogs(level='WARN') as logs:
            call_command('importdata',
                         '--base_path=campaigns/tests/test_csvs/',
                         '--num_periods=1')
        clicks = [
            Click(period=1, click_id=1, banner_id=4, campaign_id=100),
            Click(period=1, click_id=10, banner_id=3, campaign_id=100),
            Click(period=1, click_id=2, banner_id=3, campaign_id=200),
            Click(period=1, click_id=3, banner_id=2, campaign_id=300),
            Click(period=1, click_id=4, banner_id=1, campaign_id=100),
            Click(period=1, click_id=5, banner_id=4, campaign_id=200),
            Click(period=1, click_id=6, banner_id=3, campaign_id=400),
            Click(period=1, click_id=7, banner_id=2, campaign_id=400),
            Click(period=1, click_id=8, banner_id=1, campaign_id=300),
            Click(period=1, click_id=9, banner_id=4, campaign_id=200),
        ]

        loaded_clicks = Click.objects.all()
        self.assertEqual(len(loaded_clicks), 10)
        for click in clicks:
            self.assertIn(click, loaded_clicks)

    def test_load_conversions(self):
        with self.assertLogs(level='WARN') as logs:
            call_command('importdata',
                         '--base_path=campaigns/tests/test_csvs/',
                         '--num_periods=1')
        conversions = [
            Conversion(period=1, conversion_id=1, click_id_id=1, revenue=10),
            Conversion(period=1, conversion_id=2, click_id_id=1, revenue=10),
            Conversion(period=1, conversion_id=3, click_id_id=2, revenue=10),
            Conversion(period=1, conversion_id=4, click_id_id=1, revenue=10),
            Conversion(period=1, conversion_id=5, click_id_id=4, revenue=10),
            Conversion(period=1, conversion_id=6, click_id_id=7, revenue=10),
            Conversion(period=1, conversion_id=7, click_id_id=8, revenue=10),
            Conversion(period=1, conversion_id=8, click_id_id=4, revenue=10),
            Conversion(period=1, conversion_id=9, click_id_id=5, revenue=10),
            Conversion(period=1, conversion_id=10, click_id_id=10, revenue=10),
        ]

        loaded_conversions = Conversion.objects.all()
        self.assertEqual(len(loaded_conversions), 10)
        for conversion in conversions:
            self.assertIn(conversion, loaded_conversions)
