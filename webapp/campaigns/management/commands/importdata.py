import csv
import logging

from django.core.management.base import BaseCommand, CommandError

from campaigns.models import Impression, Click, Conversion

DEFAULT_BASE_PATH = 'csvs/'  # Relative to manage.py
DEFAULT_NUM_PERIODS = 4

# 1: base path, 2: period, 3: file type
PATH_TEMPLATE = '{0}/{1}/{2}_{1}.csv'

# File types
IMPRESSIONS = 'impressions'
CLICKS = 'clicks'
CONVERSIONS = 'conversions'

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports raw csv data'

    def add_arguments(self, parser):
        parser.add_argument('--base_path', default=DEFAULT_BASE_PATH)
        parser.add_argument('--num_periods', type=int, default=DEFAULT_NUM_PERIODS)

    def handle(self, *args, **options):
        rows_loaded = load_all(options['base_path'], options['num_periods'])
        logger.info(f'Processed {rows_loaded} rows.')


def load_all(base_path, num_periods):
    logger.info(f'Importing data; {base_path=}, {num_periods=}')
    rows_loaded = 0
    for period in range(1, num_periods + 1):
        rows_loaded += load_impressions(base_path, period)
        rows_loaded += load_clicks(base_path, period)
        rows_loaded += load_conversions(base_path, period)
    return rows_loaded


def load_impressions(base_path, period):
    path = make_path(base_path, period, IMPRESSIONS)
    rows = read_csv(path)
    num_rows = 0
    for row_num, row in enumerate(rows):
        num_rows += 1
        if len(row) != 2:
            raise CommandError(f'Bad row in impressions file: {path} '
                               f'Period {period} - Line {row_num + 1}')
        banner_id = int(row[0])
        campaign_id = int(row[1])
        impression = Impression(period=period, banner_id=banner_id,
                                campaign_id=campaign_id)

        if len(Impression.objects.filter(period=period, banner_id=banner_id,
                                         campaign_id=campaign_id)) > 0:
            logger.warning(f'Got duplicate impression: {impression} - '
                           f'path: {path}, line: {row_num + 1}')
            continue

        try:
            impression.save()
        except:
            raise CommandError(f'Failed to save impression: {impression} - '
                               f'path: {path}, line: {row_num + 1}')

        logger.debug(f'Impression saved: {impression}')

    return num_rows


def load_clicks(base_path, period):
    path = make_path(base_path, period, CLICKS)
    rows = read_csv(path)
    num_rows = 0
    for row_num, row in enumerate(rows):
        num_rows += 1
        if len(row) != 3:
            raise CommandError(f'Bad row in clicks file: {path} '
                               f'Period {period} - Line {row_num + 1}')
        click_id = int(row[0])
        banner_id = int(row[1])
        campaign_id = int(row[2])
        click = Click(period=period, click_id=click_id,
                      banner_id=banner_id, campaign_id=campaign_id)

        if len(Click.objects.filter(click_id=click_id)) > 0:
            logger.warning(f'Got duplicate click: {click} - '
                           f'path: {path}, line: {row_num + 1}')
            continue

        try:
            click.save()
        except:
            raise CommandError(f'Failed to save click: {click} - '
                               f'path: {path}, line: {row_num + 1}')

        logger.debug(f'Click saved: {click}')

    return num_rows


def load_conversions(base_path, period):
    path = make_path(base_path, period, CONVERSIONS)
    rows = read_csv(path)
    num_rows = 0
    for row_num, row in enumerate(rows):
        num_rows += 1
        if len(row) != 3:
            raise CommandError(f'Bad row in clicks file: {path} '
                               f'Period {period} - Line {row_num + 1}')
        conversion_id = int(row[0])
        click_id = int(row[1])
        revenue = float(row[2])
        conversion = Conversion(period=period, conversion_id=conversion_id,
                                click_id_id=click_id, revenue=revenue)

        if len(Conversion.objects.filter(conversion_id=conversion_id)) > 0:
            logger.warning(f'Got duplicate conversion: {conversion} - '
                           f'path: {path}, line: {row_num + 1}')
            continue

        try:
            conversion.save()
        except:
            raise CommandError(f'Failed to save conversion: {conversion} - '
                               f'path: {path}, line: {row_num + 1}')

        logger.debug(f'Conversion saved: {conversion}')

    return num_rows


def make_path(base_path, period, file_type):
    return PATH_TEMPLATE.format(base_path, period, file_type)


def read_csv(path, skip_headers=True):
    with open(path) as csv_file:
        if skip_headers:
            csv_file.readline()
        reader = csv.reader(csv_file)
        for row in reader:
            yield row
