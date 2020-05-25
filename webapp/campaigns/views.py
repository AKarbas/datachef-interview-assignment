from django.shortcuts import render
from django.http import HttpResponse

CAMPAIGN_TEMPLATE_NAME = 'campaigns/campaign.html'


def campaign(request, campaign_id):
    context = {
        'campaign_id': campaign_id,
        'banner_id': 102,
    }
    return render(request, CAMPAIGN_TEMPLATE_NAME, context)


def banner(request, banner_id):
    return HttpResponse(f'Banner ID: {banner_id}')
