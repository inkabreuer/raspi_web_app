from __future__ import unicode_literals

from django.db import models


class HubCache(models.Model):
    timestamp = models.DateTimeField(primary_key=True, blank=True)
    temp_reg = models.FloatField(blank=True, null=True)
    light_reg_l = models.FloatField(blank=True, null=True)
    light_reg_h = models.FloatField(blank=True, null=True)
    status_reg = models.FloatField(blank=True, null=True)
    on_board_temp_reg = models.FloatField(blank=True, null=True)
    on_board_humidity_reg = models.FloatField(blank=True, null=True)
    on_board_sensor_error = models.FloatField(blank=True, null=True)
    bmp280_temp_reg = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_l = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_m = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_h = models.FloatField(blank=True, null=True)
    bmp280_status = models.FloatField(blank=True, null=True)
    human_detect = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hub_cache'


class HubData(models.Model):
    timestamp = models.DateTimeField(primary_key=True, blank=True)
    temp_reg = models.FloatField(blank=True, null=True)
    light_reg_l = models.FloatField(blank=True, null=True)
    light_reg_h = models.FloatField(blank=True, null=True)
    status_reg = models.FloatField(blank=True, null=True)
    on_board_temp_reg = models.FloatField(blank=True, null=True)
    on_board_humidity_reg = models.FloatField(blank=True, null=True)
    on_board_sensor_error = models.FloatField(blank=True, null=True)
    bmp280_temp_reg = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_l = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_m = models.FloatField(blank=True, null=True)
    bmp280_pressure_reg_h = models.FloatField(blank=True, null=True)
    bmp280_status = models.FloatField(blank=True, null=True)
    human_detect = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hub_data'
