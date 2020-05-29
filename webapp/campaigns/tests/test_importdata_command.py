from django.core.management import call_command
from django.test import TestCase


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
