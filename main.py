from common_vars import *
from imports import *

import modules.general

bot.run(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
