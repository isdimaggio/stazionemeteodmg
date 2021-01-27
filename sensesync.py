#!/usr/bin/python3
import yaml
import mysql.connector
import time
import requests
from dateutil.parser import parse
from xml.dom import minidom

with open('config.yaml', 'r') as ymlconfig:
    config = yaml.load(ymlconfig, Loader=yaml.FullLoader)

print("[i] Letto file di configurazione")

sqlink = mysql.connector.connect(
    host=config["db_address"],
    port=config["db_port"],
    user=config["db_user"],
    password=config["db_pass"],
    database=config["db_name"]
)

q = sqlink.cursor()
q.execute("CREATE TABLE IF NOT EXISTS `" + config["db_table"] + "` (id_meteo int(10) NOT NULL auto_increment, date date NOT NULL, time time NOT NULL, temp float NOT NULL, press float NOT NULL, umidit float NOT NULL, PRIMARY KEY (id_meteo));")

print("[i] Connesso al database...")

def fetch(): 
    xmldata = requests.get(config["sensor_endpoint"])
    xdp = minidom.parseString(xmldata.text)
    xml_date = xdp.getElementsByTagName("date")[0].firstChild.nodeValue
    xml_time = xdp.getElementsByTagName("time")[0].firstChild.nodeValue
    xml_temp = xdp.getElementsByTagName("temp")[0].firstChild.nodeValue
    xml_press = xdp.getElementsByTagName("press")[0].firstChild.nodeValue
    xml_umidit = xdp.getElementsByTagName("umidit")[0].firstChild.nodeValue
    dt = parse(xml_date + ", " + xml_time)
    insert = ("INSERT INTO `" + config["db_table"] + "` (date, time, temp, press, umidit) VALUES (%s, %s, %s, %s, %s);")
    insertdata = (dt.date(), dt.time(), float(xml_temp), float(xml_press), float(xml_umidit))
    q = sqlink.cursor()
    q.execute(insert, insertdata)
    sqlink.commit()
    log = "[{}][{}] - Nuova lettura dal sensore: Temperatura={} C°, Pressione={} Kpa, Umidità={} %".format(xml_date, xml_time, xml_temp, xml_press, xml_umidit)
    print(log)

while True:
    fetch()
    time.sleep(config["read_interval"])