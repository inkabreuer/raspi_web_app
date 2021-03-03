from django.shortcuts import render
from django.http import HttpResponse

from . import models


# Create your views here.
def gpio(request):
    return HttpResponse('GPIO OUTPUT!')


def display_HubData(request):
    data = models.HubData.objects.all()  # Collect all records from table
    columns = list()
    for column in data:
        row = list()
        row.append(str(column.timestamp))
        row.append(column.temp_reg)
        row.append(column.light_reg_l)
        row.append(column.light_reg_h)
        row.append(column.status_reg)
        row.append(column.on_board_temp_reg)
        row.append(column.on_board_humidity_reg)
        row.append(column.on_board_sensor_error)
        row.append(column.bmp280_temp_reg)
        row.append(column.bmp280_pressure_reg_l)
        row.append(column.bmp280_pressure_reg_m)
        row.append(column.bmp280_pressure_reg_h)
        row.append(column.bmp280_status)
        row.append(column.human_detect)
        columns.append(str(row))
    response_html = '<br>'.join(columns)
    return HttpResponse(response_html)


def display_HubCache(request):
    data = models.HubCache.objects.all()  # Collect all records from table
    columns = list()
    for column in data:
        row = list()
        row.append(str(column.timestamp))
        row.append(column.temp_reg)
        row.append(column.light_reg_l)
        row.append(column.light_reg_h)
        row.append(column.status_reg)
        row.append(column.on_board_temp_reg)
        row.append(column.on_board_humidity_reg)
        row.append(column.on_board_sensor_error)
        row.append(column.bmp280_temp_reg)
        row.append(column.bmp280_pressure_reg_l)
        row.append(column.bmp280_pressure_reg_m)
        row.append(column.bmp280_pressure_reg_h)
        row.append(column.bmp280_status)
        row.append(column.human_detect)
        columns.append(str(row))
    response_html = '<br>'.join(columns)
    return HttpResponse(response_html)