from datetime import datetime
import socket


def log(text):
    now = datetime.now()
    with open('log.log', 'a', encoding='utf-8') as log_file:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        log_file.write(f"{ip}({hostname}) - {now} : {text} \n")


