import socket
import threading

import pika

import modules_dao


class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        self.modules = modules_dao.StudentModulesDao()
        self.connection = pika.BlockingConnection(
            #    pika.ConnectionParameters(host='localhost'))
            pika.ConnectionParameters(host='172.17.0.1'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='letter_box')

        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def send_packet(self, msg):  # method to send packet to client
        self.c_socket.send(bytes(str(msg), 'UTF-8'))  # send packet to client

    def on_receive_packet(self):  # method to receive packet from client
        data = self.c_socket.recv(2048)
        return data.decode()  # return decoded packet

    def add_to_queue(self, msg):
        self.channel.basic_publish(exchange='',
                                   routing_key='letter_box',
                                   body="Initial Data from client: " + str(msg))

    def run(self):
        # Data access object, contains modules dictionary

        print("Connection from : ", clientAddress)

        self.channel.basic_publish(exchange='', routing_key='letter_box',
                                   body='Connection from : ' + str(clientAddress))
        while True:
            msg = self.on_receive_packet()  # receive initial packet to see connection status
            print("Initial Data from client: ", msg)
            self.add_to_queue(msg)
            self.send_packet(
                msg)  # send initial status packet back to client to see connection status
            eXit_loop = False
            while not eXit_loop:
                received_module_id = None
                valid_module_id = False
                while not valid_module_id:  # flag to check if module id packet sent from client is valid/exists
                    # receive module id packet sent from client
                    received_module_id = self.on_receive_packet()
                    module_id = self.modules.id_exists(
                        module_id=received_module_id)  # check if module id sent from client exists in dictionary
                    self.add_to_queue(module_id)
                    if module_id != True:  # if doesn't exists
                        print(received_module_id)
                        # send failure status back to client
                        self.send_packet(module_id)
                    else:  # if it does exist
                        valid_module_id = True  # set flag to true and exit loop

                # send success status back to client
                self.send_packet(module_id)
                module_contents = self.on_receive_packet()
                self.add_to_queue(module_id)
                end_lo_loop = False
                if module_contents == "L":
                    while not end_lo_loop:  # if the user wants to access learning outcomes section

                        process_list_name = "learning_outcomes"

                        contents_items = self.modules.to_string_list(module_id=received_module_id,
                                                                     listname=process_list_name)  # get list of module content subitems and convert them to string
                        # send string of subitems to client as a packet
                        self.send_packet(contents_items)
                        # get CRUD action that the client wants to perform
                        crud_contents_actions = self.on_receive_packet()
                        print(crud_contents_actions)
                        self.add_to_queue(crud_contents_actions)
                        if crud_contents_actions == "A":  # if the user wants to add a new subitem to learning outcomes section
                            # get the new subitem information the user wants to enter
                            new_module_contents_item = self.on_receive_packet()
                            self.add_to_queue(new_module_contents_item)
                            result = self.modules.add_lo_element(module_id=received_module_id,
                                                                 info=new_module_contents_item)  # attempt entering that information
                            # send the result of the attempt to client as a packet
                            self.send_packet(result)
                        if crud_contents_actions == "E":  # if the user wants to edit existing subitem in learning outcomes section
                            # get the index of the subitem information the user wants to edit
                            edit_module_contents_item = self.on_receive_packet()
                            self.add_to_queue(edit_module_contents_item)

                            subitem_index = None
                            valid_subitem_index = False
                            while not valid_subitem_index:  # flag to check if module id packet sent from client is valid/exists
                                # subitem_index = self.on_receive_packet()  # receive module contents subitem index packet sent from client
                                result = self.modules.list_item_exists(
                                    module_id=received_module_id,
                                    list_name=process_list_name,
                                    list_item=int(
                                        edit_module_contents_item))  # check if module id sent from client exists in dictionary

                                if result != True:  # if doesn't exists
                                    print(result)
                                    # send failure status back to client
                                    self.send_packet(result)
                                else:  # if it does exist
                                    valid_subitem_index = True  # set flag to true and exit loop
                            self.send_packet(result)

                            # receive module contents subitem index packet sent from client
                            subitem_index_new_data = self.on_receive_packet()
                            self.add_to_queue(subitem_index_new_data)

                            result = self.modules.edit_lo_element(module_id=received_module_id,
                                                                  listname=process_list_name,
                                                                  index=int(
                                                                      edit_module_contents_item),
                                                                  new_info=subitem_index_new_data)
                            self.send_packet(result)

                        if crud_contents_actions == "D":
                            # get the index of the subitem information the user wants to edit
                            edit_module_contents_item = self.on_receive_packet()
                            self.add_to_queue(edit_module_contents_item)

                            subitem_index = None
                            valid_subitem_index = False
                            while not valid_subitem_index:  # flag to check if module id packet sent from client is valid/exists
                                # subitem_index = self.on_receive_packet()  # receive module contents subitem index packet sent from client
                                print(subitem_index)
                                result = self.modules.list_item_exists(
                                    module_id=received_module_id,
                                    list_name=process_list_name,
                                    list_item=int(
                                        edit_module_contents_item))  # check if module id sent from client exists in dictionary

                                if result != True:  # if doesn't exists
                                    print(result)
                                    # send failure status back to client
                                    self.send_packet(result)
                                else:  # if it does exist
                                    valid_subitem_index = True  # set flag to true and exit loop
                            self.send_packet(result)

                            result = self.modules.delete_lo_element(module_id=received_module_id,
                                                                    index=int(edit_module_contents_item))
                            print(result)
                            self.send_packet(result)

                        if crud_contents_actions == "R":
                            end_lo_loop = True

                if module_contents == "C":
                    process_list_name = "courses"
                    contents_items = self.modules.to_string_list(module_id=received_module_id,
                                                                 listname=process_list_name)
                    self.send_packet(contents_items)
                if module_contents == "A":
                    process_list_name = "assessments"
                    contents_items = self.modules.to_string_list(module_id=received_module_id,
                                                                 listname=process_list_name)
                    self.send_packet(contents_items)
                if module_contents == "X":
                    eXit_loop = True
                    self.send_packet("Goodbye")

            print("Client at ", clientAddress, " disconnected...")


HOSTADDR = "0.0.0.0"
PORT = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOSTADDR, PORT))

print("Server started")
print("Waiting for client request..")

counter = 0

while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()
