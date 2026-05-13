from utils.config import Config
from utils.homewizard import HomeWizard


homewizard = HomeWizard( Config.get("homewizard.ip") )

power = homewizard.get_active_power()

print(power)