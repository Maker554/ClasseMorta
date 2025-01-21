
from classeVivaManager import Session
from button import CallBack
import util


class LoginCall(CallBack):

    def __init__(self, mail, password):
        super().__init__()
        self.mail = mail
        self.password = password

    def run(self):
        session = Session()
        session.login(self.mail, self.password)
        session.getGradesData()
        return session

class LogoutCall(CallBack):

    def run(self):
        file = open("credentials.txt", "w", encoding="utf-8")
        file.write("")
        file.close()
        return True