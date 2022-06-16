import telepot
from picamera import PiCamera
from datetime import datetime
from time import sleep
from telepot.loop import MessageLoop
from subprocess import call
import time

print('Pausa de inicio')
time.sleep(10)
print('conexion')
camera = PiCamera()

def handle(msg):
    global telegramText
    global chat_id
    global receiveTelegramMessage
    
    chat_id = msg['chat']['id']
    telegramText = msg['text']
    print('Message Received from ' + str(chat_id))
    
    if telegramText == "/start":
        bot.sendMessage(chat_id, "Bot raspberry iniciado '/start' para iniciar 'FOTO' para tomar una foto 'VIDEO' para tomar un video '/stop' para apagar")
    
    else:
        receiveTelegramMessage = True
        

bot = telepot.Bot('5319258738:AAFHJxfwk0Amkx0kyYlZdQYrIdJJqzQMpXk')
bot.message_loop(handle)

print('Telegram esta listo')
receiveTelegramMessage = False
sendTelegramMessage = False

try:
    while True:
        if receiveTelegramMessage == True:
            receiveTelegramMessage = False
            if telegramText == "FOTO":
                print("FOTO")
                bot.sendMessage(chat_id, 'CAPTURANDO IMAGEN')
                camera.capture('./capture.jpg')
                bot.sendPhoto(chat_id=chat_id, photo=open('./capture.jpg', 'rb'))
            elif telegramText == "VIDEO":
                print("VIDEO")
                bot.sendMessage(chat_id, 'GRABANDO VIDEO')
                camera.start_recording('video.h264')
                sleep(5)
                camera.stop_recording()
                command = "MP4Box -add " + 'video.h264' + " " + 'videotelegram.mp4'
                print(command)
                call([command], shell=True)
                bot.sendVideo(chat_id, video = open('videotelegram.mp4', 'rb'))
            elif telegramText == "/stop":
                print("Apagando")
                bot.sendMessage(chat_id, 'APAGANDO...')
                bot.sendMessage(chat_id, 'BOT APAGADO')
                exit()
            
except Exception as e:
    print(e)
finally:
    camera.close()
                



