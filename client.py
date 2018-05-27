from socket import *
from sys import argv

def main():
    # Parse command line args
    if len(argv) != 3 or not argv[2].isdigit():
        print("usage: python3 client.py <server name> <server port>")
        return 1

    hostname, serverTCPPort = argv[1], int(argv[2])
    print("Client is running...")
    print("Remote host: {}, remote TCP port: {}".format(hostname, serverTCPPort))

    # Prompt user for their name
    username = input("Please enter your lovely name: ") #A.A

    # Create TCP socket
    TCPclientsocket = socket(AF_INET, SOCK_STREAM) #A.A

    # Get IP address of server via DNS and print it
    TCPaddr = (hostname, serverTCPPort) #AA
    print('The server address is {}:{}'.format(TCPaddr[0], TCPaddr[1])) #AA
    
    # Connect to the server program
    TCPclientsocket.connect(TCPaddr) #AA

    # Send hello message to the server over TCP connection
    TCPclientsocket.send("hello {}".format(username).encode()) #AA

    # TCP Loop
    while True:
        # Read in from TCP port
        input1 = TCPclientsocket.recv(2048) #aa 

        # Keep listening if it doesn't receive a portUDP message
        if input1.startswith(b'gameport '):
            # Read the control message from the TCP socket and print its contents
            # Split message in two words separated by space, assign the second word to UDPport
            _, UDPport = input1.decode().split(' ')
            UDPport = int(UDPport)
            print('Received UDP port#: {}'.format(UDPport))
            # Break from loop once needed info is received
            break


    # Create a UDP socket
    UDPsocket = socket(AF_INET, SOCK_DGRAM) #AA A- Not sure if this should be part fo the loop above
    UDPaddr = (hostname, UDPport)
    print(UDPaddr)
    end = False # default end flag

    # Game loop
    while True:
        # Prompt
        command = input(">")
        valid_commands = ['start', 'end', 'guess', 'exit']
        # Validate the command
        if not any(command.startswith(x) for x in valid_commands):
            # If not valid, ignore and continue asking
            continue

        # Parse command
        if command.startswith('start'):
            UDPsocket.sendto(b'ready', UDPaddr)
        elif command.startswith('end'):
            UDPsocket.sendto(b'end', UDPaddr)
        elif command.startswith('guess'):
            UDPsocket.sendto(command.encode(), UDPaddr)
        elif command.startswith('exit'):
            UDPsocket.sendto(b'bye', UDPaddr)
            end = True

        # UDP loop
        while True:
            # Continuously Read in from UDP port
            incoming, _ = UDPsocket.recvfrom(4096)

            # print message
            # print('Message received: {}'.format(incoming))

            if incoming.startswith(b'instr'):
                text = incoming[6:]  # Text = message without the first 6 characters ('instr ')
                print(text.decode())
                # Instruction message should be followed by stat message
                incoming, _ = UDPsocket.recvfrom(4096)
                _, text1, text2 = incoming.split(b' ')
                print('Word: {} Attempts left: {}'.format(text1.decode(), text2.decode()))
                
            elif incoming.startswith(b'stat'):
                _, text1, text2 = incoming.split(b' ')
                print('Word: {} Attempts left: {}'.format(text1.decode(), text2.decode()))
                
            elif incoming.startswith(b'end'):
                text = incoming[4:]
                print(text.decode())
                
            elif incoming.startswith(b'bye'):
                # Send bye message and exit
                UDPsocket.sendto(b'bye', UDPaddr)
                end = True
                
            elif incoming.startswith(b'na'):
                pass
                
            # Break once receiving info and reprompt user
            break

        # If end message received, end client process
        if end:
            break

    # Close sockets
    print("Closing TCP and UDP sockets...")

 ###########################################

if __name__ == "__main__":
    main()