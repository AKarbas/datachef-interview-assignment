from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Impression, Click, Conversion
from ..views import Campaign


class CampaignViewTests(TestCase):

    def test_no_campaign(self):
        response = self.client.get(reverse('campaigns:campaign', args=(1,)))
        self.assertContains(response, 'Campaign not found', status_code=404)

    def test_show_single_banner(self):
        banner_id = 2
        campaign_id = 2
        period = current_period()
        create_impression(period, banner_id, campaign_id)
        response = self.client.get(reverse('campaigns:campaign',
                                           args=(campaign_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['campaign_id'], campaign_id)
        self.assertEqual(response.context['banner_id'], banner_id)

        response2 = self.client.get(reverse('campaigns:campaign',
                                            args=(campaign_id,)))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.context['campaign_id'], campaign_id)
        self.assertEqual(response2.context['banner_id'], banner_id)

    def test_more_than_ten_banners_with_revenue(self):
        campaign_id = 3
        period = current_period()
        banner_count = 11
        for x in range(1, banner_count + 1):
            create_impression(period, x, campaign_id)
            create_click(period, x, x, campaign_id)
            create_conversion(period, x, x, x)

        candidates = Campaign.candidate_banners(period, campaign_id)
        accepted_candidates = Campaign.accepted_banners(candidates)

        self.assertEqual(len(accepted_candidates), 10)
        for x, candidate in enumerate(accepted_candidates):
            self.assertEqual(candidate, banner_count - x)

    def test_five_to_ten_banners_with_revenue(self):
        campaign_id = 4
        period = current_period()
        banner_count = 11
        banners_with_revenue = 8
        for x in range(1, banners_with_revenue + 1):
            create_impression(period, x, campaign_id)
            create_click(period, x, x, campaign_id)
            create_conversion(period, x, x, x)
        for x in range(banners_with_revenue + 1, banner_count + 1):
            create_impression(period, x, campaign_id)
            create_click(period, x, x, campaign_id)

        candidates = Campaign.candidate_banners(period, campaign_id)
        accepted_candidates = Campaign.accepted_banners(candidates)

        self.assertEqual(len(accepted_candidates), banners_with_revenue)
        for x, candidate in enumerate(accepted_candidates):
            self.assertEqual(candidate, banners_with_revenue - x)

    def test_less_than_five_banners_with_revenue(self):
        campaign_id = 5
        period = current_period()
        banner_count = 8
        banners_with_revenue = 3
        for x in range(1, banner_count - banners_with_revenue + 1):
            create_impression(period, x, campaign_id)
            for y in range(1, x + 1):
                click_id = x ** 2 + y
                create_click(period, click_id, x, campaign_id)
        for x in range(banner_count - banners_with_revenue + 1, banner_count + 1):
            click_id = banner_count ** 2 + x
            create_impression(period, x, campaign_id)
            create_click(period, click_id, x, campaign_id)
            create_conversion(period, x, click_id, x)

        candidates = Campaign.candidate_banners(period, campaign_id)
        accepted_candidates = Campaign.accepted_banners(candidates)

        self.assertEqual(len(accepted_candidates), 5)
        for x, candidate in enumerate(accepted_candidates):
            self.assertEqual(candidate, banner_count - x)

    def test_five_banners_with_clicks(self):
        campaign_id = 6
        period = current_period()
        banner_count = 8
        banners_with_clicks = 5
        for x in range(1, banners_with_clicks + 1):
            create_impression(period, x, campaign_id)
            for y in range(1, x + 1):
                click_id = x ** 2 + y
                create_click(period, click_id, x, campaign_id)
        for x in range(banners_with_clicks + 1, banner_count + 1):
            create_impression(period, x, campaign_id)

        candidates = Campaign.candidate_banners(period, campaign_id)
        accepted_candidates = Campaign.accepted_banners(candidates)

        self.assertEqual(len(accepted_candidates), 5)
        for x, candidate in enumerate(accepted_candidates):
            self.assertEqual(candidate, banners_with_clicks - x)

    def test_less_than_five_banners_with_clicks(self):
        campaign_id = 7
        period = current_period()
        banner_count = 8
        banners_with_clicks = 3
        for x in range(1, banners_with_clicks + 1):
            create_impression(period, x, campaign_id)
            for y in range(1, x + 1):
                click_id = x ** 2 + y
                create_click(period, click_id, x, campaign_id)
        for x in range(banners_with_clicks + 1, banner_count + 1):
            create_impression(period, x, campaign_id)

        candidates = Campaign.candidate_banners(period, campaign_id)
        accepted_candidates = Campaign.accepted_banners(candidates)

        self.assertEqual(len(accepted_candidates), 5)
        for x in range(banners_with_clicks):
            self.assertEqual(accepted_candidates[x], banners_with_clicks - x)


def create_impression(period, banner_id, campaign_id):
    return Impression.objects.create(period=period, banner_id=banner_id,
                                     campaign_id=campaign_id)


def create_click(period, click_id, banner_id, campaign_id):
    return Click.objects.create(period=period, click_id=click_id,
                                banner_id=banner_id, campaign_id=campaign_id)


def create_conversion(period, conversion_id, click_id, revenue):
    return Conversion.objects.create(period=period,
                                     conversion_id=conversion_id,
                                     click_id_id=click_id, revenue=revenue)


def current_period():
    now_minutes = timezone.localtime().minute
    return (now_minutes // 15) + 1
