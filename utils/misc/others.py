import random
import time

def check(llist: list) -> int:
    random_number = random.randint(1000000, 9999999)
    if random_number in llist:
        llist.remove(random_number)
        time.sleep(0.05)
        return check(llist)
    else:
        return random_number