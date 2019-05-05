PORT=/dev/tty.SLAB_USBtoUART

upload:
	ampy --port $(PORT) --baud 115200 put micropython-configurator/configurator.py 
	ampy --port $(PORT) --baud 115200 put config.json 
	ampy --port $(PORT) --baud 115200 put main.py
