
"""
"""

# Native
import datetime
import time
import random

# 3rd-Party

# Proprietary
from models.account import Account
from models.tavern import Tavern

import deploy

from db import session

from config import config


account = Account()

session.add(account)

update_period = config['settings']['update']
do_refresh = True
last_update = 0

while True:

    if do_refresh:
        print "----------------------------------------------------"
        print "%s" % datetime.datetime.today()
        account.fetch()
        session.commit()

        #break
        print "Players: %s" % (len(account.players))

        print "Buildings: %s" % (len(account.city.buildings))

        print "Taverns: %s" % (len(account.taverns))

        print "Money: %s" % "{:,}".format(account.resources.money)

        print "Supplies: %s" % "{:,}".format(account.resources.supplies)

        for tavern in account.taverns:
            tavern.sit()
        #
        for player in account.players:
            player.aid()

        Tavern.collect()

        session.commit()

        last_update = time.time()
        do_refresh = False

    print "Checking... (%d)" % (update_period - (time.time() - last_update))
    # NOTE: The full update should adjust for any coins/supplies/resources gained from these pickups
    account.city.pickup()

    account.city.produce()

    session.commit()

    sleep = random.randrange(10, 30)

    time.sleep(sleep)

    do_refresh = time.time() - last_update > update_period
