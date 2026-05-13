from utils.config import Config
from utils.homewizard import HomeWizard
from utils.marstek import MarstekClient
from utils.openhab import OpenHAB
import time

marstek = MarstekClient(Config.get("marstek.ip"), Config.get("marstek.port"))
homewizard = HomeWizard( Config.get("homewizard.ip") )
openhab = OpenHAB( Config.get("openhab.url") )

while True:
    state = openhab.get_item_state("active_power state")
    print(f"Get:  {state}  ")

    #     power = homewizard.get_active_power()
    #     setPower = 0-power
    #     setPower = max(-2500, min(2500, setPower))
    #     if marstek.es_set_mode_passive(power= setPower, cd_time=10):
    #         print(f"Set power to {setPower} W for 10 seconds")
    #     else:
    #         print("✗ Failed to set mode")

    time.sleep(10)
