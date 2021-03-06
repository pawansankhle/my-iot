
import logger
import gc
gc.collect()

import utime
import machine
from machine import Pin
from machine import Timer

# Init global variables
motion_on = False
turn_off_delay = 10
last_motion_time = 0

send_message = 0
 
def init_wifi():
    import wifi
    wifi.init()
    wifi.disable_wifi_ap()

def init_config():
    import config
    config.initialize_config()

def pin_interrupt():
	global motion_on, last_motion_time, send_message
	current_d1 = d1.value()
	
	# Motion detected, update time
	if (current_d1):
		last_motion_time = utime.time()
				
		if (motion_on == False):
			# Motion hasn't been triggered yet, send motion on
			motion_on = True
			send_message = 1
			
def send_motion_message():
	global motion_on
	if (motion_on):
		pub.on_pub('on')
	else:
		pub.on_pub('off')

def check_update():
	import update
	update.start()

def update_device_status():
	pub.on_pub('ONLINE','device/status')

# init config files
logger.initialize_logging('micro.log')

# initailize app config
init_config()

# init wifi and connect
init_wifi()

#  check new update
check_update()

import mqtt
mqtt._connect()
import mqtt_pub as pub

update_device_status()

# Setup d1 (pin 5)			
d1 = Pin(5, Pin.IN)
d1.irq(handler=lambda p:pin_interrupt(), trigger=Pin.IRQ_RISING)

while(True):
	current_d1 = d1.value()
	
	if (motion_on and current_d1 == 0 and utime.time() - last_motion_time > turn_off_delay):
		# Motion hasn't timed out yet, no motion currently detected, and time has elapsed
		motion_on = False
		send_message = 1
			
	# Send message
	if (send_message):
		send_message = 0
		send_motion_message()
		update_device_status()
		
	utime.sleep_ms(1000)
    




