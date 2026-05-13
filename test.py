from utils.config import Config
from utils.homewizard import HomeWizard


config = Config()


homewizard = HomeWizard(config.get("homewizard"))

power = homewizard.get_active_power()

print(power)