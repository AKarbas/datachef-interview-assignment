import logging

from random import choice as random_choice

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

CAMPAIGN_TEMPLATE_NAME = 'campaigns/campaign.html'
BANNER_NAME_TEMPLATE = 'image_{}.png'

SQL_QUERY_TEMPLATE = '''select imp.banner_id,
       count(clk.click_id)  as clk_count,
       SUM(cnv.revenue)     as revenue
from campaigns_impression as imp
         LEFT JOIN campaigns_click as clk
                   on imp.period = clk.period
                       and imp.banner_id = clk.banner_id
                       and imp.campaign_id = clk.campaign_id
         LEFT JOIN campaigns_conversion as cnv
                   on clk.click_id = cnv.click_id_id
where imp.period = %s
  and imp.campaign_id = %s
GROUP BY imp.banner_id
ORDER BY revenue desc, clk_count desc
LIMIT 10;
'''

logger = logging.getLogger(__name__)


class Campaign(View):
    def get(self, request, campaign_id):
        period = Campaign.current_period()
        with connection.cursor() as cursor:
            cursor.execute(SQL_QUERY_TEMPLATE, [period, campaign_id])
            rows = cursor.fetchall()
        banner_id = Campaign.get_banner_id_from_db_result(rows)
        banner_name = BANNER_NAME_TEMPLATE.format(banner_id)
        context = {
            'campaign_id': campaign_id,
            'banner_id': banner_id,
            'banner_name': banner_name,
        }
        return render(request, CAMPAIGN_TEMPLATE_NAME, context)

    @staticmethod
    def current_period():
        now_minutes = timezone.localtime().minute
        return (now_minutes // 15) + 1

    @staticmethod
    def get_banner_id_from_db_result(result_rows):
        accepted_banners = []
        for row in result_rows:
            if row[2] or len(accepted_banners) < 5:
                # Banner has revenue or less than 5 banners accepted
                accepted_banners.append(row[0])
        logger.debug(f'{accepted_banners=}')
        return random_choice(accepted_banners)
