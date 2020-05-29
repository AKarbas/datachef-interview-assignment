from django.db import models


class Impression(models.Model):
    period = models.PositiveSmallIntegerField(db_index=True)
    banner_id = models.PositiveIntegerField(db_index=True)
    campaign_id = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return (f'Period: {self.period}, '
                f'BannerId: {self.banner_id}, '
                f'CampaignId: {self.campaign_id}')


class Click(models.Model):
    period = models.PositiveSmallIntegerField(db_index=True)
    click_id = models.PositiveIntegerField(db_index=True, primary_key=True)
    banner_id = models.PositiveIntegerField(db_index=True)
    campaign_id = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return (f'Period: {self.period}, '
                f'ClickId: {self.click_id}, '
                f'BannerId: {self.banner_id}, '
                f'CampaignId: {self.campaign_id}')


class Conversion(models.Model):
    period = models.PositiveSmallIntegerField(db_index=True)
    conversion_id = models.PositiveIntegerField(db_index=True, primary_key=True)
    click_id = models.ForeignKey(Click, on_delete=models.SET_NULL, null=True)
    revenue = models.FloatField()

    def __str__(self):
        return (f'Period: {self.period}, '
                f'ConversionId: {self.conversion_id}, '
                f'ClickId: {self.click_id}, '
                f'Revenue: {self.revenue}')
