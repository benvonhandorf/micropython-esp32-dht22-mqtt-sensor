upload:
	ampy --port /dev/ttyUSB0 put micropython-configurator/configurator.py 
	ampy --port /dev/ttyUSB0 put ../shared-config/config.json 
	ampy --port /dev/ttyUSB0 put main.py
