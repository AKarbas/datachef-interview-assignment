import logging

from random import choice as random_choice

from django.core.cache import cache
from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.views import View

logger = logging.getLogger(__name__)


class Campaign(View):
    TEMPLATE_NAME = 'campaigns/campaign.html'
    BANNER_NAME_TEMPLATE = 'image_{}.png'
    LAST_BANNER_KEY = 'last_banner'
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

    def get(self, request, campaign_id):
        period = Campaign.current_period()
        candidate_banners = Campaign.get_candidate_banners_from_db(period,
                                                                   campaign_id)
        last_banner = Campaign.get_last_banner(request)
        banner_id = Campaign.get_banner_id_from_db_result(candidate_banners,
                                                          last_banner)
        Campaign.set_last_banner(request, banner_id)
        banner_name = Campaign.BANNER_NAME_TEMPLATE.format(banner_id)
        context = {
            'campaign_id': campaign_id,
            'banner_id': banner_id,
            'banner_name': banner_name,
        }
        return render(request, Campaign.TEMPLATE_NAME, context)

    @staticmethod
    def current_period():
        now_minutes = timezone.localtime().minute
        return (now_minutes // 15) + 1

    @staticmethod
    def get_last_banner(request):
        return (request.session[Campaign.LAST_BANNER_KEY]
                if Campaign.LAST_BANNER_KEY in request.session
                else None)

    @staticmethod
    def set_last_banner(request, banner_id):
        request.session[Campaign.LAST_BANNER_KEY] = banner_id

    @staticmethod
    def get_candidate_banners_from_db(period, campaign_id):
        cache_key = f'{period}:{campaign_id}'
        if (cached_res := cache.get(cache_key)) is not None:
            return cached_res
        with connection.cursor() as cursor:
            cursor.execute(Campaign.SQL_QUERY_TEMPLATE, [period, campaign_id])
            res = cursor.fetchall()
        cache.set(cache_key, res)
        return res

    @staticmethod
    def get_banner_id_from_db_result(result_rows, last_banner=None):
        accepted_banners = []
        for row in result_rows:
            if row[2] or len(accepted_banners) < 5:
                # Banner has revenue or less than 5 banners accepted
                accepted_banners.append(row[0])
        if last_banner in accepted_banners and len(accepted_banners) > 1:
            accepted_banners.remove(last_banner)
        logger.debug(f'{accepted_banners=}')
        return random_choice(accepted_banners)
