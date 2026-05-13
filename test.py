from utils.config import Config
from utils.homewizard import HomeWizard
from utils.marstek import MarstekClient

marstek = MarstekClient(Config.get("marstek.ip"), Config.get("marstek.port"))
homewizard = HomeWizard( Config.get("homewizard.ip") )


while True:
    power = homewizard.get_active_power()
    setPower = 0-power
    if client.es_set_mode_passive(power= setPower, cd_time=10):
        print(f"Set power to {setPower} W for 10 seconds")
    else:
        print("✗ Failed to set mode")

    time.sleep(10)
