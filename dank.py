import pyautogui, time, threading, random
pyautogui.FAILSAFE = True

time.sleep(3)

postmeme = ['f', 'r', 'i', 'c', 'k']

def type(arg):
    pyautogui.write(arg, interval=0.05)
    time.sleep(0.08)
    pyautogui.press('enter')
    time.sleep(0.1)

def deposit():
    type('pls dep max')

#######################################

def fourty_five_sec():
    global fourty_five_sec_idle
    while True:
        if fourty_sec_idle == True:
            fourty_five_sec_idle = False
            type('pls beg')
            deposit()
            fourty_five_sec_idle = True
            time.sleep(46)
        else:
            time.sleep(2.5)

def fourty_sec():
    global fourty_sec_idle
    while True:
        if fourty_five_sec_idle == True:
            fourty_sec_idle = False
            type('pls fish')
            type('pls hunt')
            type('pls dig')
                
            type('pls postmeme')
            time.sleep(0.18)
            type(random.choice(postmeme))

            deposit()
            fourty_sec_idle = True
            time.sleep(41)
        else:
            time.sleep(2)

def trivia():
    while True:
        type('pls triv')
        time.sleep(random.uniform(1, 9))
        type(random.choice(['A', 'B', 'C', 'D']))
        time.sleep(random.uniform(16, 1000))

#######################################

#t1 = threading.Thread(target=fourty_five_sec)
#t2 = threading.Thread(target=fourty_sec)
#fourty_sec_idle = True
#fourty_five_sec_idle = False

#t1.start()
#t2.start()


trivia()
