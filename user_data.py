# user_data.py
import random
import time
import json

def create_user(threadIndex: int, loopIndex: int, birthDay: int, birthMonth: int):
    with open('inputs/user_data.json', 'r') as file:
        user_data = json.load(file)

    currentTimestamp = time.time()
    return dict(
        email='%s%sL%dT%d%s' % (random.choice(user_data['firstNameStore']),
                                hex(int(currentTimestamp)),
                                loopIndex,
                                threadIndex,
                                random.choice(user_data['emailStore'])),
        password=user_data['passwordStore'],
        firstName=random.choice(user_data['firstNameStore']),
        lastName=random.choice(user_data['lastNameStore']),
        birthDay=birthDay,
        birthMonth=birthMonth
    )
