from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import spidev
from RPi import GPIO
import time
from subprocess import check_output



class Database:
    def __init__(self, app, user, password, db, host='localhost', port=3306):
        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = db
        app.config['MYSQL_DATABASE_HOST'] = host

        mysql = MySQL(cursorclass=DictCursor)  # cursor is dict ipv tuple
        mysql.init_app(app)
        self.mysql = mysql

    def get_data(self, sql, params=None, single=False):
        # Deze routine wordt gebruikt om data op te halen.
        # Params kunnen leeg zijn
        conn = self.mysql.connect()
        cursor = conn.cursor()
        result = None

        print("Getting data")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            if single:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
        conn.close()

        # We always return the data as a big list to keep this as generic as possible 😉
        return result

    def set_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print("Creating / Updating data")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return 'Error: {e}'
        conn.close()

        return cursor.lastrowid

    def delete_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print("Deleting data")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return 'Error: {e}'

        conn.close()

        return cursor.rowcount

class Mcp3008:
    def read_channel(self,channel):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 10 ** 5
        datalist = [1, (8 + channel) << 4,0]
        bytes_in = spi.xfer2(datalist)
        a = bytes_in[1]
        b = bytes_in[2]
        result = a << 8 | b
        spi.close()
        return result

class Ds1820:

    def __init__(self,sensor_file_name='/sys/bus/w1/devices/28-041661c404ff/w1_slave'):
        self.sensor_file_name = sensor_file_name
        self.__temperature = 0.0
        self.test = 'bla'

    def temperature(self):
        sensor_file = None
        try:
            sensor_file = open(self.sensor_file_name, 'r')
            for line in sensor_file:
                pos = line.find('t=')
                if pos != -1:
                    string_temperature = line[pos:]
                    self.__temperature = float(string_temperature[2:]) / 1000


        except Exception  as e:
            print(e)
        finally:
            if sensor_file != None:
                sensor_file.close()
            return  self.__temperature

    def __str__(self):
        return "De temperatuur is {} \N{DEGREE SIGN} Celsius".format(self.temperature)


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


conn = Database(app=app, user='lander', password='Lander', host='localhost', db='Project')
print(conn)

endpoint = '/api/v1'

DB0 = 16
DB1 = 12
DB2 = 25
DB3 = 24
DB4 = 23
DB5 = 26
DB6 = 19
DB7 = 13
I1 = 17
I2 = 27
E = 22
LCD_E = 20
LCD_RS = 21

LCD_PINS = [16,12,25,24,23,26,19,13]

ips = check_output(['hostname', '--all-ip-addresses'])
mcp = Mcp3008()
temp = Ds1820()
sensor_file_name = '/sys/bus/w1/devices/28-041661c404ff/w1_slave'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(I1, GPIO.OUT)
GPIO.setup(I2, GPIO.OUT)
GPIO.setup(E, GPIO.OUT)

pwm = GPIO.PWM(E, 100)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LCD_PINS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.output(LCD_RS, GPIO.HIGH)
    GPIO.output(LCD_E, GPIO.HIGH)


    for PIN in LCD_PINS:
        GPIO.setup(PIN,GPIO.OUT)

def set_data_value(value):
    mask=0x01
    for i in range(0,8):
        if (value&mask ==0):
            GPIO.output(LCD_PINS[i],0)
        else:
            GPIO.output(LCD_PINS[i], 1)
        mask = mask <<1


def send_instruction(value):
    GPIO.output(LCD_E,1)
    GPIO.output(LCD_RS, 0)
    set_data_value(value)
    GPIO.output(LCD_E, 0)
    time.sleep(0.1)

def send_character(value):
    GPIO.output(LCD_E,1)
    GPIO.output(LCD_RS, 1)
    set_data_value(value)
    GPIO.output(LCD_E, 0)
    time.sleep(0.01)

def LCD_Init():
    send_instruction(0x38)#function instruction
    send_instruction(0x01)#clear display
    send_instruction(0xF)#display on

def sendip():
    waarde = str(ips)
    naam = "SmartCurtains"
    waard = waarde[2:16]
    send_character(0x49)  # I
    send_character(0x50)  # P
    send_character(0x3A)
    for i in waard:
         send_character(ord(i))

def sendnaam():
    naam = "SmartCurtains"
    for i in naam:
        send_character(ord(i))

try:
    setup()
    LCD_Init()
    sendnaam()
    send_instruction(0xC0)
    sendip()
    # my_pwm = GPIO.PWM(motor1A, 100)
    # my_pwm.start(0)
    # time.sleep(1)
    # my_pwm.ChangeDutyCycle(80)
    # time.sleep(10)
    # GPIO.output(motor1A, GPIO.HIGH)
    # GPIO.output(motor1B, GPIO.LOW)
    # time.sleep(1)
    # GPIO.output(motor1A, GPIO.LOW)
    # pwm = GPIO.PWM(Enable,100)
    # pwm.start(0)
    # GPIO.output(motor1A, True)
    # GPIO.output(motor1B, False)
    # pwm.ChangeDutyCycle(60)
    # GPIO.output(Enable, True)
    # time.sleep(2)
    # GPIO.output(Enable, False)
    # GPIO.output(motor1A, False)
    # GPIO.output(motor1B, True)
    # pwm.ChangeDutyCycle(75)
    # GPIO.output(Enable,True)
    # time.sleep(3)
    # pwm.stop()

except KeyboardInterrupt:
    GPIO.cleanup()


@app.route(endpoint + '/')
def get_data():
    return "Build to route"

@app.route(endpoint + '/temperatuur', methods=['GET'])
def temperatuur():
    if request.method == 'GET':
        data = conn.get_data("SELECT concat(date(datumofentry),' ', time(datumofentry)) as Dag, concat(waarde,'°C') as Temp FROM Project.Meting where sensorid = 3 order by MetingID desc limit 10;")
        return jsonify(data), 200

@app.route(endpoint + '/lichtsterkte', methods=['GET'])
def lichtsterkte():
    if request.method == 'GET':
        data = conn.get_data("SELECT concat(date(datumofentry),' ', time(datumofentry)) as Dag, concat(waarde,'%') as licht FROM Project.Meting where sensorid = 1 order by MetingID desc limit 10;")
        return jsonify(data), 200

@app.route(endpoint + '/uv', methods=['GET'])
def uv():
    if request.method == 'GET':
        data = conn.get_data("SELECT concat(date(datumofentry),' ', time(datumofentry)) as Dag, concat(waarde,'nm') as uv FROM Project.Meting where sensorid = 2 order by MetingID desc limit 10;")
        return jsonify(data), 200

@app.route(endpoint + '/index', methods=['GET'])
def index():
    if request.method == 'GET':
        data = conn.get_data("SELECT round(waarde) as temp FROM Project.Meting where SensorID = 3 order by datumofentry desc limit 1;")
        data += conn.get_data("SELECT round(waarde) as licht FROM Project.Meting where SensorID = 1 order by datumofentry desc limit 1;")
        data += conn.get_data("SELECT round(waarde) as uv FROM Project.Meting where SensorID = 2 order by datumofentry desc limit 1;")
        return jsonify(data), 200

@app.route(endpoint + '/gewilde', methods=['GET'])
def gewilde_temperatuur():
    if request.method == 'GET':
        data = conn.get_data("SELECT gewildeTemperatuur as temp FROM Project.Log order by idLog desc limit 1;")
        return jsonify(data), 200

@app.route(endpoint + '/meting/log/<waarde>', methods=['PUT'])
def instellen_temperatuur(waarde):
    if request.method == 'PUT':
        conn.set_data("insert into Log(gewildeTemperatuur) values (%s)" % waarde)
        return "gelukt"


@app.route(endpoint + '/meting', methods=['PUT'])
def metingdata():
    if request.method == 'PUT':
        temperatuur = temp.temperature()
        temperatuur = round(temperatuur,2)
        resp1 = mcp.read_channel(0)
        resp3 = mcp.read_channel(2)
        answer1 = 100 - (resp1 / 1023.0 * 100)
        answer1 = round(answer1, 2)
        conn.set_data("insert into Meting(SensorID, Waarde, DatumOfEntry) values (1,%s,now())" % answer1)
        conn.set_data("insert into Meting(SensorID, Waarde, DatumOfEntry) values (2,%s,now())" % resp3)
        conn.set_data("insert into Meting(SensorID, Waarde, DatumOfEntry) values (3,%s,now())" % temperatuur)
        return "gesaved"


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)



