from django.test import TestCase
from django.urls import reverse

class CampaignViewTests(TestCase):
    def test_no_campaign(self):
        response = self.client.get(reverse('campaigns:campaign', args=(1,)))
        self.assertContains(response, 'Campaign not found', status_code=404)

