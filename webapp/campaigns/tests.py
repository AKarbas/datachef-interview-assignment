from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Impression


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


def create_impression(period, banner_id, campaign_id):
    return Impression.objects.create(period=period, banner_id=banner_id,
                                     campaign_id=campaign_id)


def current_period():
    now_minutes = timezone.localtime().minute
    return (now_minutes // 15) + 1
