import smbus2
import datetime
import time
import psycopg2
import os

# Zu Hardware verbinden
DEVICE_BUS = 1
DEVICE_ADDR = 0x17

TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D

bus = smbus2.SMBus(DEVICE_BUS)

# Connect to Postgres Docker
connection = psycopg2.connect("dbname='postgres' user='postgres' password='hunter2' host='db' port='5432'")
cursor = connection.cursor()


def get_postgres_insert_query(database_name):
    return """ INSERT INTO """ + database_name + """ (timestamp, temp_reg, light_reg_l, light_reg_h, status_reg, 
            on_board_temp_reg, on_board_humidity_reg, on_board_sensor_error, bmp280_temp_reg, bmp280_pressure_reg_l, 
            bmp280_pressure_reg_m, bmp280_pressure_reg_h, bmp280_status, human_detect) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


def table_exists(table_name, cursor=cursor):
    exists = False
    try:
        command = """SELECT
            EXISTS(SELECT
            1
            FROM
            information_schema.tables
            WHERE
            table_name = '""" + table_name + """');
            """
        cursor.execute(command)
        exists = cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(e)
    return exists


def init_table(database_name, con=connection, cursor=cursor):
    try:
        command = """
            CREATE TABLE """ + database_name + """ (
                timestamp TIMESTAMP, 
                temp_reg REAL, 
                light_reg_l REAL, 
                light_reg_h REAL, 
                status_reg REAL, 
                on_board_temp_reg REAL, 
                on_board_humidity_reg REAL, 
                on_board_sensor_error REAL, 
                bmp280_temp_reg REAL, 
                bmp280_pressure_reg_l REAL, 
                bmp280_pressure_reg_m REAL, 
                bmp280_pressure_reg_h REAL, 
                bmp280_status REAL, 
                human_detect INTEGER
            )
            """
        cursor.execute(command)
        con.commit()
        print(f'Tabelle {database_name} angelegt.')
    except psycopg2.Error as e:
        print(e)


def get_a_recieve_buf():
    a_receive_buf = [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')]
    for i in range(TEMP_REG, HUMAN_DETECT + 1):
        a_receive_buf.append(bus.read_byte_data(DEVICE_ADDR, i))
    print(a_receive_buf)
    return a_receive_buf


def insert_row(database_name, row, con=connection, cursor=cursor):
    try:
        cursor.execute(get_postgres_insert_query(database_name=database_name), row)
        con.commit()
        count = cursor.rowcount
        print(count, f"Record inserted successfully into table {database_name}")

    except (Exception, psycopg2.Error) as error:
        if (con):
            print(f"Failed to insert record into table {database_name}", error)


def collect_last_minute_raw_data(con=connection, cursor=cursor):
    def for_loop(ende):
        for i in range(0, ende):
            insert_row(database_name="hub_cache", row=get_a_recieve_buf())
            time.sleep(1)

    init_table(database_name='hub_cache')
    ende=False
    if os.environ['run_mode'] == "dev":
        ende = 5
        for_loop(ende=ende)
    elif os.environ['run_mode'] == "prod":
        ende = 60
        for_loop(ende=ende)
    return True


def calculate_last_minute_data(con=connection, cursor=cursor):
    """Aggregation über die letzte Minute raw_hub_data"""
    command = """
                SELECT max(timestamp) as timestamp
                , avg(temp_reg) as temp_reg
                , avg(light_reg_l) as light_reg_l 
                , avg(light_reg_h) as light_reg_h 
                , avg(status_reg) as status_reg 
                , avg(on_board_temp_reg) as on_board_temp_reg 
                , avg(on_board_humidity_reg) as on_board_humidity_reg 
                , max(on_board_sensor_error) as on_board_sensor_error 
                , avg(bmp280_temp_reg) as bmp280_temp_reg 
                , avg(bmp280_pressure_reg_l) as bmp280_pressure_reg_l 
                , avg(bmp280_pressure_reg_m) as bmp280_pressure_reg_m 
                , avg(bmp280_pressure_reg_h) as bmp280_pressure_reg_h 
                , avg(bmp280_status) as bmp280_status 
                , max(human_detect) as human_detect 
                from hub_cache
                ;"""
    cursor.execute(command)
    agg_minute_row = cursor.fetchall()
    return agg_minute_row[0]


def drop_table(database_name, con=connection, cursor=cursor):
    command = """DROP TABLE """ + database_name + """;"""
    cursor.execute(command)
    con.commit()
    if table_exists(table_name=database_name) is False:
        print(f'Dropped table {database_name}.')
    return True


def run():
    if table_exists(table_name='hub_data') is False:
        init_table(database_name='hub_data')
    if table_exists(table_name='hub_cache'):
        drop_table(database_name='hub_cache')
    collect_last_minute_raw_data()
    last_minute_data = calculate_last_minute_data()
    insert_row(database_name="hub_data", row=last_minute_data)


if __name__ == "__main__":
    print('HERE')
    if os.environ['run_mode'] == "prod":
        while True:
            run()
    elif os.environ['run_mode'] == 'dev':
        run()
    else:
        print("Kein richtiger run_mode")
        print(os.environ['run_mode'])
        print(type(os.environ['run_mode']))
        print(os.environ['run_mode']=="dev")

'''    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if aReceiveBuf[STATUS_REG] & 0x01 :
    print("Off-chip temperature sensor overrange!")
elif aReceiveBuf[STATUS_REG] & 0x02 :
    print("No external temperature sensor!")
else :
    print("Current off-chip sensor temperature = %d Celsius" % aReceiveBuf[TEMP_REG])


if aReceiveBuf[STATUS_REG] & 0x04 :
    print("Onboard brightness sensor overrange!")
elif aReceiveBuf[STATUS_REG] & 0x08 :
    print("Onboard brightness sensor failure!")
else :
    print("Current onboard sensor brightness = %d Lux" % (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]))

print("Current onboard sensor temperature = %d Celsius" % aReceiveBuf[ON_BOARD_TEMP_REG])
print("Current onboard sensor humidity = %d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])

if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
    print("Onboard temperature and humidity sensor data may not be up to date!")

if aReceiveBuf[BMP280_STATUS] == 0 :
    print("Current barometer temperature = %d Celsius" % aReceiveBuf[BMP280_TEMP_REG])
    print("Current barometer pressure = %d pascal" % (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
else :
    print("Onboard barometer works abnormally!")

if aReceiveBuf[HUMAN_DETECT] == 1 :
    print("Live body detected within 5 seconds!")
else:
    print("No humans detected!")
header = ['TEMP_REG', 
          'LIGHT_REG_L', 
          'LIGHT_REG_H', 
          'STATUS_REG', 
          'ON_BOARD_TEMP_REG', 
          'ON_BOARD_HUMIDITY_REG',
          'ON_BOARD_SENSOR_ERROR',
          'BMP280_TEMP_REG',
          'BMP280_PRESSURE_REG_L',
          'BMP280_PRESSURE_REG_M',
          'BMP280_PRESSURE_REG_H',
          'BMP280_STATUS',
          'HUMAN_DETECT']
'''
