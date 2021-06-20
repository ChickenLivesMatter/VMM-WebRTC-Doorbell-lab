import argparse
import asyncio
import logging
import os
import random
import names
import cv2
import async_timeout
from av import VideoFrame

# this email and passord was created for lab purpose only
# Email you want to send the notification from (only works with gmail)
FROM_EMAIL = 'sender@gmail.com'
FROM_EMAIL_PASSWORD = '123wmTEST'
# Email you want to send the update to
TO_EMAIL = 'walid.massaoudi@heig-vd.ch'
from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
# Asynchrones function to handle recievded messages
def asyQueue(signalingType, rx):
    queue = asyncio.Queue()
    for signal in rx:
        signalingType.on(signal, lambda content, signal=signal: queue.put_nowait((signal, content)))
    return queue
class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class Email:
    def __init__(self, sender, subject, preamble, body):
        self.sender = sender
        self.subject = subject
        self.preamble = preamble
        self.body = body

    def send(self, to_email):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.sender.email
        msgRoot['To'] = to_email
        msgRoot.preamble = self.preamble

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgText = MIMEText(self.body)
        msgAlternative.attach(msgText)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.sender.email, self.sender.password)
        smtp.sendmail(self.sender.email, to_email, msgRoot.as_string())
        smtp.quit(
#send an email with the conference url    
def send_email_notification(url):
        sender = EmailSender(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        email = Email(
            sender,
            'Video Doorbell',
            'Notification: A visitor is waiting',
            'A video doorbell caller is waiting on the virtual meeting room. Meet them at %s' % url
        )
        email.send(TO_EMAIL)

async def main():
 while(1):
    #1. Wait until keypress (to be replaced later by the pushbutton press event)
    print("press the button")
    #2. Connect to the signaling server.
    print("connecting to server")
    sio = socketio.AsyncClient(ssl_verify=False)
    await sio.connect('https://localhost:443')
    #3. Join a conference room with a random name (send 'create' signal with room name).
    room = names.get_full_name()
    await sio.emit('join',room)
    # wait for a new message on the queue
     queue = receiver_queue(sio, messages=["invite","new_peer","created","joined",  "full",  "ice_candidate", "bye"])
     message = await queue.get()
    #4. Wait for response. If response is 'joined' or 'full', stop processing and return to the loop. Go on if response is 'created'.
    if message[0] in ("full", "joined") : 
            print(message[0],"wainting for response")
            time.sleep(10)
            await sio.disconnect()
            await sio.wait()
    if message[0] == "created" :
            print("room  created !!!")
    #5. Send a message (SMS, Telegram, email, ...) to the user with the room name. Or simply start by printing it on the terminal. 
    ## this function not finished yet
      #send_email_notification(chatID)
    

    #6. Wait (with timeout) for a 'new_peer' message. If timeout, send 'bye' to signaling server and return to the loop. 
    if answer[0] != 'new_peer':
        print(message[0],"fail !")
            time.sleep(10)
    #7. Wait (with timeout) for an 'invite' message. If timemout, send 'bye to signaling server and return to the loop.         
    if answer[0] != 'new_peer':
    print(message[0],"fail !")
        time.sleep(10)      
    #8. Acquire the media stream from the Webcam.      
    video_player = MediaPlayer('/dev/video0', format='v4l2', options={'video_size': '320x240'})
    audio_player = MediaPlayer("default", format="pulse")
    if message[0] == "invite" : 
    #  9. Create the PeerConnection and add the streams from the local Webcam.
            remoteOffer = message[1]
            pc = RTCPeerConnection()
            pc.addTrack(video_player)
            pc.addTrack(audio_player)
            #  10. Add the SDP from the 'invite' to the peer connection.
            pc.setRemoteDescription(remoteOffer)
            answer = await pc.createAnswer()
            #  11. Generate the local session description (answer) and send it as 'ok' to the signaling server.
            pc.setLocalDescription(answer)
            answer = pc.localDescription
            await sio.emit("ok",answer)
        # 12. Wait (with timeout) for a 'bye' message. 
        if message[0] == "bye" :
            #  13. Send a 'bye' message back and clean everything up (peerconnection, media, signaling).
            await sio.emit("bye")
            await sio.disconnect()
            pc.close()

# Python 3.7+
asyncio.run(main())    
