import configurator
import machine
import time
import os
import dht
from machine import Timer
from umqtt.simple import MQTTClient

configurator = configurator.Configurator()

class EnvironmentSensor:
  def __init__(self):
    self.sensor = dht.DHT22(machine.Pin(4))

  def setup(self, server, user, password, topic):
    self.baseTopic = topic
    self.temperatureTopic = "{0}/temperature".format(self.baseTopic)
    self.humidityTopic = "{0}/humidity".format(self.baseTopic)

    print(self.temperatureTopic)
    print(self.humidityTopic)

    self.mqtt_client = MQTTClient("env_0", server, user=user, password=password)
    print("Last will topic: " "{0}/connected".format(self.baseTopic))
    self.mqtt_client.set_last_will(bytes("{0}/connected".format(self.baseTopic), 'utf-8'), b"0")
    self.mqtt_client.connect()
    self.mqtt_client.publish(bytes("{0}/connected".format(self.baseTopic), 'utf-8'), b"1")

    self.readingTimer = Timer(-1)

    self.update()

    self.readingTimer.init(period=30000, mode=Timer.PERIODIC, callback=self.timerCallback)

  def timerCallback(self, timer):
    self.update()

  def update(self):
    self.sensor.measure()

    temp = self.sensor.temperature()
    humidity = self.sensor.humidity()

    print("Temperature: {0} Humidity: {1}".format(temp, humidity))

    self.mqtt_client.publish(bytes(self.temperatureTopic, 'utf-8'), bytes("{0}".format(temp), 'utf-8'))
    self.mqtt_client.publish(bytes(self.humidityTopic, 'utf-8'), bytes("{0}".format(humidity), 'utf-8'))

  def main(self):

    while True:
        if True:
          print("waiting for message")

          # Blocking wait for message
          self.mqtt_client.wait_msg()  
        else:
          # Non-blocking wait for message
          self.mqtt_client.check_msg()
          # Then need to sleep to avoid 100% CPU usage (in a real
          # app other useful actions would be performed instead)
          time.sleep(1)


environment_sensor = EnvironmentSensor()

def main():
  print("Configuring...")
  
  while not configurator.configureNetwork():
    machine.idle()
    time.sleep(1)
    machine.idle()
    print("Configuring...")

  print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  if configurator.wlan.isconnected():
    print("status light configuration {0} {1}".format(configurator["mqttServerIp"], configurator["mqttTopic"]))
    environment_sensor.setup(configurator["mqttServerIp"], configurator["mqttUser"], configurator["mqttPassword"], configurator["mqttTopic"])
    environment_sensor.main()

def restore() :
  os.rename("main_store.py", "main.py")
  print("Restoring main.py")
  machine.reset()

if __name__ == "__main__":
  skipBootPin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
  if(skipBootPin.value() == 0):
    os.rename("main.py", "main_store.py")
    print("Skipping initialization")
  else:
    main()  
