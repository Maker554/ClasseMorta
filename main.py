import pygame

import util
from button import Button
from callbacks import LoginCall, LogoutCall
from inputBox import InputBox
from label import Label

# pygame setup
pygame.init()
SIZE = 1.0
screen = pygame.display.set_mode((1080 * SIZE, 2340 * SIZE), pygame.RESIZABLE)
game_surface = pygame.Surface((1080 * SIZE, 2340 * SIZE))
clock = pygame.time.Clock()
running = True
MESSAGE_COUNT_DOWN = 2 * 60

title = Label("CLASSEMORTA", int(128*SIZE))

# login page elements
input_box_mail = InputBox(50*SIZE, 170*SIZE, 300*SIZE, int(90*SIZE))
input_box_password = InputBox(50*SIZE, 270*SIZE, 300*SIZE, int(90*SIZE), private=True)
login_button = Button(500, 500*SIZE, 200*SIZE, 80*SIZE, text="LOGIN",)
warning = Label("Login Failed", int(64*SIZE), "red")
message_counter = 0

# main page elements
logout_button = Button(100, 100*SIZE, 200*SIZE, 80*SIZE, text="LOGOUT",)

# datas
mail = ""
password = ""
session = None

# pages
login_page = True
main_page = False

# loading credentials
try:
    file = open("credentials.txt", "r", encoding="utf-8")
    mail = file.readline()
    password = file.readline()
    file.close()

    loginCall = LoginCall(mail, password)
    session = loginCall.run()
    if session.loggedIn:  # if the login is successful

        list = session.grades("INFORMATICA")
        print(list)
        print(util.media(list))

        login_page = False
        main_page = True

    if not session.loggedIn:
        file = open("credentials.txt", "w", encoding="utf-8")
        file.write("")
        file.close()

        message_counter = MESSAGE_COUNT_DOWN

except FileNotFoundError:
    file = open("credentials.txt", "x", encoding="utf-8")
    file.close()

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

    # drawing

    screen.fill("black")  # clear the screen

    title.draw(screen, (screen.get_width() / 2, 100 * SIZE), "center")

    if login_page:
        input_box_mail.draw(screen)
        input_box_password.draw(screen)
        login_button.draw(screen, "center")

    if main_page:
        logout_button.draw(screen, "top_left")

    # processing login
    if login_page:
        if session is not None: # if a login has been attempted
            if session.loggedIn: # if the login is successful

                #save login data
                file = open("credentials.txt", "w", encoding="utf-8")
                file.write(mail)
                file.write("\n")
                file.write(password)
                file.close()

                list = session.grades("INFORMATICA")
                print(list)
                print(util.media(list))

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