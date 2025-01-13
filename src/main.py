import os

import pygame

import util
from button import Button
from callbacks import LoginCall, LogoutCall
from encription import decode, incode
from inputBox import InputBox
from label import Label

# pygame setup
pygame.init()
SIZE = 1.0
pygame.display.set_caption('Classe Morta')
screen = pygame.display.set_mode((1080 * SIZE, 2340 * SIZE), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

PRECISION = 1
MESSAGE_COUNT_DOWN = 2 * 60
MATERIE = ["STORIA", "INFORMATICA", "LINGUA E CULTURA STRANIERA","LINGUA E LETTERATURA ITALIANA", "FILOSOFIA", "FISICA", "DISEGNO", "SCIENZE MOTORIE","SCIENZE NATURALI", "MATEMATICA", "EDUCAZIONE CIVICA"]
CREDENTIALS = util.resource_path("assets/credentials.txt")
title = Label("CLASSEMORTA", int(128*SIZE))

# login page elements
input_box_mail = InputBox(50*SIZE, 170*SIZE, 300*SIZE, int(90*SIZE))
input_box_password = InputBox(50*SIZE, 270*SIZE, 300*SIZE, int(90*SIZE), private=True)
login_button = Button(500, 500*SIZE, 200*SIZE, 80*SIZE, text="LOGIN",)
warning = Label("Login Failed", int(64*SIZE), "red")
message_counter = 0

# main page elements
logout_button = Button(100, 200*SIZE, 250*SIZE, 80*SIZE, text="LOGOUT",)

materie_labels = []
for i in MATERIE:
    nome = i
    if nome == "LINGUA E LETTERATURA ITALIANA":
        nome = "ITALIANO"
    if nome == "LINGUA E CULTURA STRANIERA":
        nome = "INGLESE"
    materie_labels.append(Label(nome, int(64*SIZE)))

voti_labels = []
for i in MATERIE:
    voti_labels.append(Label("", int(70*SIZE)))

# datas
mail = ""
password = ""
session = None

# pages
login_page = True
main_page = False

# loading credentials
try:
    file = open(CREDENTIALS, encoding="utf-8")
    mail = decode(file.readline())
    in_ = decode(file.readline())
    password = in_ [1 : len(in_)]  # strange problem, a space is added at beginning of password
    print(mail)
    print(password)
    file.close()

    loginCall = LoginCall(mail, password)
    session = loginCall.run()
    if session.loggedIn:  # if the login is successful

        for i in range(len(MATERIE)):
            list = session.grades(MATERIE[i])
            media = util.media(list)
            voti_labels[i].change_text((str(media) [0 : (2 + PRECISION)]))


        login_page = False
        main_page = True

    if not session.loggedIn:
        file = open(CREDENTIALS, "w", encoding="utf-8")
        file.write("")
        file.close()

        message_counter = MESSAGE_COUNT_DOWN

except FileNotFoundError:
    file = open(CREDENTIALS, "x", encoding="utf-8")
    file.close()

# creating labels

# MAIN LOOP

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN: # quit on ESC
            if event.key == pygame.K_ESCAPE:
                running = False

        if login_page:

            if event.type == pygame.KEYDOWN and input_box_mail.active and event.key == pygame.K_RETURN:
                input_box_password.set_active(True)
            else:
                input_box_password.handle_event(event) # input is not handled when activated by switching from email input box

            # update and handle other input boxes
            input_box_mail.handle_event(event)
            input_box_mail.update()
            input_box_password.update()

            if event.type == pygame.KEYDOWN:
                mail = input_box_mail.text
                password = input_box_password.text

            # create session from login button
            session = login_button.handle_event(event, LoginCall(mail, password))

        if main_page:
            value = logout_button.handle_event(event, LogoutCall())
            if value is not None:
                login_page = True
                main_page = False
                session = None
                input_box_mail.text = ""
                input_box_password.text = ""

    # drawing

    screen.fill("black")  # clear the screen

    title.draw(screen, (screen.get_width() / 2, 100 * SIZE), "center")

    if login_page:
        input_box_mail.draw(screen)
        input_box_password.draw(screen)
        login_button.draw(screen, "center")

    if main_page:
        logout_button.draw(screen, "top_left")

        if session is not None:
            for i in range(len(materie_labels)):
                materie_labels[i].draw(screen, (100, (400 + i*100)*SIZE))
                voti_labels[i].draw(screen, (screen.get_width() - 200, (400 + i*100)*SIZE))

    # processing login
    if login_page:
        if session is not None: # if a login has been attempted
            if session.loggedIn: # if the login is successful

                #save login data
                file = open(CREDENTIALS, "w", encoding="utf-8")
                file.write(incode(mail))
                file.write("\n")
                file.write(incode(password))
                file.close()

                for i in range(len(MATERIE)):
                    list = session.grades(MATERIE[i])
                    media = util.media(list)
                    voti_labels[i].change_text((str(media)[0: (2 + PRECISION)]))



                login_page = False
                main_page = True

            if not session.loggedIn:
                message_counter = MESSAGE_COUNT_DOWN

        if message_counter > 0:
            message_counter -= 1
            warning.draw(screen, (screen.get_width() / 2, screen.get_height() - 200), "red")

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()