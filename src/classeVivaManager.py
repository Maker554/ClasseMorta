import requests

CUT_POINT = 8500 #10004
IDENTIFIER = '<p align="center" class="s_reg_testo cella_trattino" style="height:40px; line-height:40px; border:0; margin:0; padding:0;font-weight:bold; font-size:22px;">'

class Session:

    web_session = requests.Session()

    username: str
    name: str
    id: str
    cid: str
    loggedIn: bool = False
    mail: str
    password: str
    grades_data: str = "empty"

    def login(self, mail, password):

        if mail == "" or password == "":
            return False

        result = self.web_session.post(
            url="https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php?a=aLoginPwd",
            headers={
                "Host": "web.spaggiari.eu",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Referer": "https://web.spaggiari.eu/home/app/default/login.php",
                "Origin": "https://web.spaggiari.eu",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Alt-Used": "web.spaggiari.eu",
                "name": "value"
            },
            data="cid=&uid=" + mail + "&pwd=" + password + "&pin=&target="
        ).json()

        data = result['data']['auth']
        accountInfo = data['accountInfo']
        self.loggedIn = data['loggedIn']

        if self.loggedIn:

            self.username = accountInfo['cognome']
            self.name = accountInfo['nome']
            self.id = accountInfo['id']
            self.cid = accountInfo['cid']

            self.mail = mail
            self.password = password

    def getGradesData(self):
        result = self.web_session.get(
            url="https://web.spaggiari.eu/cvv/app/default/genitori_note.php?ordine=materia&filtro=tutto"
        )
        self.grades_data = result.text[CUT_POINT: len(result.text)]


    def grades(self, materia: str):
        if self.grades_data != "empty":
            list = []

            pos = self.grades_data.find(materia)
            string = self.grades_data[pos : len(self.grades_data)]
            pos = string.find('<tr class="" valign="middle" align="center" height="38">')
            string = string[0: pos - 7]

            while(len(string) > 100):

                pos = string.find(IDENTIFIER)
                sub_string = string[pos + len(IDENTIFIER): len(string)]
                string = sub_string
                pos = sub_string.find('</p')
                sub_string = sub_string[1: pos-1]

                if len(sub_string) == 3:
                    list.append(9.75)
                if len(sub_string) == 2:
                    if sub_string[1] == "+":
                        list.append(float(sub_string[0]) + 0.25)
                    if sub_string[1] == "-":
                        list.append(float(sub_string[0]) - 0.25)
                    if sub_string[1] == "½":
                        list.append(float(sub_string[0]) + 0.5)
                    if sub_string == "10":
                        list.append(10.0)
                elif len(sub_string) == 1:
                    if sub_string == 'g' or sub_string == 'a':
                        pass
                    else:
                        list.append(float(sub_string))

            return list

    def printGradesData(self):
        print(self.grades_data)

#session = Session()
#session.login("mattincoped@gmail.com","MMmm55@@")
#session.getGradesData()
#print(session.printGradesData())

# STORIA, INFORMATICA, LINGUA E CULTURA STRANIERA,
# LINGUA E LETTERATURA ITALIANA, FILOSOFIA,
# FISICA, DISEGNO, SCIENZE MOTORIE,
# SCIENZE NATURALI, MATEMATICA, EDUCAZIONE CIVICA