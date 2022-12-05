import socket
import threading

from dao import modules_dao


class ClientThread(threading.Thread):

    def send_packet(self, msg):  # method to send packet to client
        self.c_socket.send(bytes(str(msg), 'UTF-8'))  # send packet to client

    def on_receive_packet(self):  # method to receive packet from client
        data = self.c_socket.recv(2048)
        return data.decode()  # return decoded packet

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def run(self):
        modules = modules_dao.StudentModulesDao()  # Data access object, contains modules dictionary
        print("Connection from : ", clientAddress)
        while True:
            msg = self.on_receive_packet()  # receive initial packet to see connection status
            print("Data from client: ", msg)
            self.send_packet(
                msg)  # send initial status packet back to client to see connection status

            eXit_loop = False
            while not eXit_loop:
                received_module_id = None
                valid_module_id = False
                while not valid_module_id:  # flag to check if module id packet sent from client is valid/exists
                    received_module_id = self.on_receive_packet()  # receive module id packet sent from client
                    module_id = modules.id_exists(
                        module_id=received_module_id)  # check if module id sent from client exists in dictionary
                    if module_id != True:  # if doesn't exists
                        print(received_module_id)
                        self.send_packet(module_id)  # send failure status back to client
                    else:  # if it does exist
                        valid_module_id = True  # set flag to true and exit loop

                self.send_packet(module_id)  # send success status back to client

                module_contents = self.on_receive_packet()

                end_lo_loop = False
                while not end_lo_loop:
                    if module_contents == "L":  # if the user wants to access learning outcomes section

                        process_list_name = "learning_outcomes"

                        contents_items = modules.to_string_list(module_id=received_module_id,
                                                                listname=process_list_name)  # get list of module content subitems and convert them to string
                        self.send_packet(contents_items)  # send string of subitems to client as a packet
                        crud_contents_actions = self.on_receive_packet()  # get CRUD action that the client wants to perform
                        print(crud_contents_actions)
                        if crud_contents_actions == "A":  # if the user wants to add a new subitem to learning outcomes section
                            new_module_contents_item = self.on_receive_packet()  # get the new subitem information the user wants to enter
                            result = modules.add_lo_element(module_id=received_module_id,
                                                            info=new_module_contents_item)  # attempt entering that information
                            self.send_packet(result)  # send the result of the attempt to client as a packet
                        if crud_contents_actions == "E":  # if the user wants to edit existing subitem in learning outcomes section
                            edit_module_contents_item = self.on_receive_packet()  # get the index of the subitem information the user wants to edit

                            subitem_index = None
                            valid_subitem_index = False
                            while not valid_subitem_index:  # flag to check if module id packet sent from client is valid/exists
                                # subitem_index = self.on_receive_packet()  # receive module contents subitem index packet sent from client
                                print(subitem_index)
                                result = modules.list_item_exists(
                                    module_id=received_module_id,
                                    list_name=process_list_name,
                                    list_item=int(
                                        edit_module_contents_item))  # check if module id sent from client exists in dictionary

                                if result != True:  # if doesn't exists
                                    print(result)
                                    self.send_packet(result)  # send failure status back to client
                                else:  # if it does exist
                                    valid_subitem_index = True  # set flag to true and exit loop
                            self.send_packet(result)

                            subitem_index_new_data = self.on_receive_packet()  # receive module contents subitem index packet sent from client

                            result = modules.edit_lo_element(module_id=received_module_id,
                                                             listname=process_list_name,
                                                             index=int(edit_module_contents_item),
                                                             new_info=subitem_index_new_data)
                            self.send_packet(result)

                        if crud_contents_actions == "D":
                            edit_module_contents_item = self.on_receive_packet()  # get the index of the subitem information the user wants to edit

                            subitem_index = None
                            valid_subitem_index = False
                            while not valid_subitem_index:  # flag to check if module id packet sent from client is valid/exists
                                # subitem_index = self.on_receive_packet()  # receive module contents subitem index packet sent from client
                                print(subitem_index)
                                result = modules.list_item_exists(
                                    module_id=received_module_id,
                                    list_name=process_list_name,
                                    list_item=int(
                                        edit_module_contents_item))  # check if module id sent from client exists in dictionary

                                if result != True:  # if doesn't exists
                                    print(result)
                                    self.send_packet(result)  # send failure status back to client
                                else:  # if it does exist
                                    valid_subitem_index = True  # set flag to true and exit loop
                            self.send_packet(result)

                            result = modules.delete_lo_element(module_id=received_module_id,
                                                               index=int(edit_module_contents_item))
                            print(result)
                            self.send_packet(result)

                        if crud_contents_actions == "R":
                            end_lo_loop = True

                if module_contents == "C":
                    process_list_name = "courses"
                    contents_items = modules.to_string_list(module_id=received_module_id,
                                                            listname=process_list_name)
                    self.send_packet(contents_items)
                if module_contents == "A":
                    process_list_name = "assessments"
                    contents_items = modules.to_string_list(module_id=received_module_id,
                                                            listname=process_list_name)
                    self.send_packet(contents_items)
                if module_contents == "X":
                    eXit_loop = True
                    self.send_packet("Goodbye")

        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 64001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

counter = 0

while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()
