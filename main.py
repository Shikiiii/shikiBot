from common_vars import *
from imports import *

import modules.general
import modules.economy
import modules.events
import modules.eh
import modules.botowner

bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
