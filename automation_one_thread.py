# automation_one_thread.py
from new_account import create
from user_data import create_user
from proxy_data import create_proxy
import csv, time
from datetime import date, datetime

def create_thread(threadIndex: int, accountPerThread: int):
    for i in range(accountPerThread):
        timeStart = time.time()
        proxy = create_proxy()
        userInformations = create_user(threadIndex=threadIndex, loopIndex=i, birthDay=10, birthMonth=5)
        print('Thread %d:%d Start %s \n %s \n' % (threadIndex, i, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), userInformations))
        try:
            isSuccess = create(proxy, userInformations, threadIndex=threadIndex, loopIndex=i)
            if isSuccess:
                print('Thread %d:%d Success Create %s' % (threadIndex, i, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                exportAccountToCsv(threadIndex, userInformations)
                timeCreat = time.time() - timeStart
                print('Thread %d:%d End Succes Import CSV in %ss %s \n' % (threadIndex, i, timeCreat, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                print('Thread %d:%d End Failed %s \n' % (threadIndex, i, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        except Exception as e:
            print('Thread %d:%d End Failed %s \n' % (threadIndex, i, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print(e)

def exportAccountToCsv(threadIndex: int, userInformations: dict):
    CsvFileName = 'outputs/%s-Thread%d-account.csv' % (date.today(), threadIndex)
    with open(CsvFileName, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([userInformations['email'], userInformations['password'], userInformations['firstName'], userInformations['lastName'], userInformations['birthDay'], userInformations['birthMonth']])
