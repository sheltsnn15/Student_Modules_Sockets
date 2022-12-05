import socket

from datatype import enums

LCAX_VALIDATION = ['L', 'C', 'A', 'X']
AEDR_VALIDATION = ['A', 'E', 'D', 'R']


# client class

def get_module_id():  # get the module id from dictionary
    valid_choice = False  # flag to check if user input is correct
    while not valid_choice:  # loop until user input is correct
        module_id = input(f"{enums.OTHER_QUESTIONS.ENTER_MOD_ID.value}")  # get user input
        if module_id.isdigit():  # check if input is disgit
            print(f"{enums.OTHER_QUESTIONS.INVALID_INPUT.value} Input must not be an integer")  # display error message
        else:
            valid_choice = True  # set flag to true and exit the loop
    return str(module_id)  # return the user input


def get_user_choice(correct, **kwargs):  # get choice for all other program functions
    valid_choice = False  # flag to check if user input is correct
    while not valid_choice:  # loop until user input is correct
        choice = input(str(f"\n{enums.to_string(kwargs['ENUM_'])}? ")).upper()  # get user input
        if choice in correct:  # check if input is disgit
            valid_choice = True  # set flag to true and exit the loop
        else:
            print(f"{choice} is an invalid choice.\n")  # display error message
    return str(choice)  # return the user input


def get_contents_index(**kwargs):  # get the module id from dictionary
    valid_choice = False  # flag to check if user input is correct
    while not valid_choice:  # loop until user input is correct
        contents_index = input(f"\n{kwargs['ENUM_']}? ")  # get user input
        if not contents_index.isdigit():  # check if input is disgit
            print(f"{enums.OTHER_QUESTIONS.INVALID_INPUT.value} Input must be an integer")  # display error message
        else:
            valid_choice = True  # set flag to true and exit the loop
    return int(contents_index)  # return the user input


def on_receive_packet():  # method to receive packet from server
    return str(client.recv(1024).decode())  # return decoded packet


def send_packet(out_data):  # method to send packet to server
    client.sendall(bytes(out_data, 'UTF-8'))  # send packet to server


def from_server_list_item_validation():
    valid_item_id = False  # flag to check if client input is valid
    while not valid_item_id:  # loop until client input is valid
        out_data = get_contents_index(ENUM_=enums.OTHER_QUESTIONS.ENTER_LO_NUM)  # get requested module id from user
        send_packet(str(out_data))  # send module requested module id to server
        module_exists = on_receive_packet()  # get module id validation message from server
        print(module_exists)  # print module id validation message from server
        if module_exists != "ID Item Not Found":  # if the module id validation message says module id requested is found
            valid_item_id = True  # set flag to true to exit loop


SERVER = "127.0.0.1"
PORT = 64001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
client.connect((SERVER, PORT))  # connect socket using localhost and port
client.sendall(bytes("This is from Client", 'UTF-8'))  # send packet to server to show connection status

while True:
    in_data = on_receive_packet()  # receive initial packet to see connection status
    print("From Server :", in_data)

    eXit_loop = False
    while not eXit_loop:
        valid_module_id = False  # flag to check if client input is valid
        while not valid_module_id:  # loop until client input is valid
            out_data = get_module_id()  # get requested module id from user
            send_packet(out_data)  # send module requested module id to server
            module_exists = on_receive_packet()  # get module id validation message from server
            print(module_exists)  # print module id validation message from server
            if module_exists != "ID Item Not Found":  # if the module id validation message says module id requested is found
                valid_module_id = True  # set flag to true to exit loop

        module_contents = get_user_choice(LCAX_VALIDATION,
                                          ENUM_=enums.VIEWS)  # get request from client to view the module id contents [(L)earning Outcomes, (C)ourses, (A)ssessments] or e(X)it the program
        send_packet(module_contents)  # send client request packet
        end_lo_loop = False
        while not end_lo_loop:
            if module_contents == "L":

                contents_items = on_receive_packet()  # get client request response packet from server
                print(contents_items)

                crud_contents_actions = get_user_choice(AEDR_VALIDATION,
                                                        ENUM_=enums.CRUD)  # get request from client to perform CRUD operations on the contents subitems [(A)dd, (E)dit, (D)elete] or (R)eturn to previous point in the program
                #  NOTE!!! client can only perform CRUD operations to the learning outcomes column
                send_packet(crud_contents_actions)
                print(crud_contents_actions)

                if crud_contents_actions == "A":  # if client want to add a new learning outcome
                    new_module_contents_item = input(
                        str(f"{enums.OTHER_QUESTIONS.NEW_LO_DESC}"))  # enter a new module content subitem
                    send_packet(new_module_contents_item)  # send it to server as a packet
                if crud_contents_actions == "E":  # if client want to add a new learning outcome

                    from_server_list_item_validation()
                    edited_module_contents_index = contents_index = input(
                        f"\n{enums.OTHER_QUESTIONS.ENTER_NEW_TEXT}? ")  # get user input
                    send_packet(edited_module_contents_index)  # send it to server as a packet

                if crud_contents_actions == "D":
                    from_server_list_item_validation()

                if crud_contents_actions == "R":
                    send_packet("R")  # send it to server as a packet
                    end_lo_loop = True

        if module_contents == "C":
            contents_items = on_receive_packet()  # get client request response packet from server
            print(contents_items)
        if module_contents == "A":
            contents_items = on_receive_packet()  # get client request response packet from server
            print(contents_items)
        if module_contents == "X":
            contents_items = on_receive_packet()  # get client request response packet from server
            print(contents_items)
            eXit_loop = True

client.close()
