import time
import logging
from datetime import datetime
from pytz import timezone
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
import schedule

# Logger setup
logging.basicConfig(filename='../watering_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# FritzBox connection setup
fc = FritzConnection(address='192.168.178.1', password='')  # enter password here
ain = ''  # assume the AIN of the switch is known

# Germany timezone
germany_timezone = timezone('Europe/Berlin')


# Function to water the plants
def water_plants(fh, ain, cycle_time_seconds):
    try:
        logging.info("Starting watering process...")
        fh.set_switch(ain, on=True)
        logging.info("Water pump turned on.")
        time.sleep(cycle_time_seconds)
        fh.set_switch(ain, on=False)
        logging.info("Water pump turned off.")
    except Exception as e:
        logging.error(f"Error occurred during watering: {str(e)}")


# Schedule watering
def schedule_watering(fh, ain, start_time, cycle_time_seconds):
    for time_slot in start_time:
        schedule.every().day.at(time_slot.strftime('%H:%M')).do(water_plants, fh=fh, ain=ain,
                                                                cycle_time_seconds=cycle_time_seconds)
        logging.info(f"Watering scheduled to start at {time_slot.strftime('%H:%M')} every day.")


if __name__ == "__main__":
    try:
        # FritzHomeAutomation instance
        fh = FritzHomeAutomation(fc)

        # Watering schedule parameters
        start_times = [
            datetime.now(germany_timezone).replace(hour=10, minute=45, second=0),  # Example start time: 08:00
            datetime.now(germany_timezone).replace(hour=11, minute=00, second=0),  # Example start time: 10:00
            datetime.now(germany_timezone).replace(hour=11, minute=20, second=0),  # Example start time: 12:00
            datetime.now(germany_timezone).replace(hour=11, minute=40, second=0),  # Example start time: 14:00
            datetime.now(germany_timezone).replace(hour=12, minute=00, second=0),  # Example start time: 16:00
            datetime.now(germany_timezone).replace(hour=12, minute=30, second=0),  # Example start time: 16:00
            datetime.now(germany_timezone).replace(hour=13, minute=00, second=0),  # Example start time: 16:00
            datetime.now(germany_timezone).replace(hour=13, minute=20, second=0),  # Example start time: 16:00
            datetime.now(germany_timezone).replace(hour=13, minute=40, second=0),  # Example start time: 16:00
            datetime.now(germany_timezone).replace(hour=14, minute=00, second=0),  # Example start time: 16:00
        ]
        cycle_time_seconds = 80  # Example cycle time: 80 seconds

        # Scheduling watering
        schedule_watering(fh, ain, start_times, cycle_time_seconds)

        # Main loop to keep script running
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
