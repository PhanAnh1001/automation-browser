# automation-browser
Python, Selenium

# python version
Only Python 3.8.13 for some library can active

# config at /inputs/config.js
Current can run only 1 thread at same time because can only open one file undected-chromedriver
"thread": {
    "quantity" : 1, // threads run at same time
    "accountPerThread" : 10, // account number a thread will create
    "isTest" : false // run thread without creat account, only generate data
},
"chromeDriver": {
    "undetected": {
        "isActive": true // use undetected chrome to avoid grid capcha
    },
    "normal" : {
        "version" : "124",
        "os" : "mac"
    }
}

# Run Python script without cache
python3 -B automation_multi_thread.py

# Doc Selenium element
