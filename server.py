from socket import *
from sys import argv
from random import *
from game import *

def main():
    # Parse command line args
    if len(argv) != 2:
        print("usage: python3 server.py <word to guess or '-r' for random word>")
        return 1

    print("Server is running...")

    # Create the TCP Socket
    print("Creating TCP socket...")
    TCPserversocket = socket(AF_INET, SOCK_STREAM)#a

    # Bind a name to the TCP socket, letting the OS choose the port number
    TCPserversocket.bind(("", 0)) #AA

    # Get the port number of the socket from the OS and print it
    # The port number will be a command-line parameter to the client program
    TCPserverport = TCPserversocket.getsockname()[1]
    print('Server is listening on port {}'.format(TCPserverport))

    # Configure the TCP socket (using listen) to accept a connection request
    TCPserversocket.listen(1) #AA

    try: # try/except to catch ctrl-c
        while True:
            # Accept the TCP Connection
            print("Waiting for a client...")
            TCPclientsocket, _ = TCPserversocket.accept()

            # TCP loop
            while True:
                # Continuously Read in from TCP port
                input1 = TCPclientsocket.recv(4096)

                # Keep listening if it doesn't receive a hello message
                if not input1.startswith(b'hello'):
                    continue

                # Extract username handling empty case
                _, username = input1.split(b' ')

                # Create and bind a UDP socket, letting the OS choose the port number
                print("Creating UDP socket...")
                UDPsocket = socket(AF_INET, SOCK_DGRAM)
                UDPsocket.bind(("", 0))

                # Add a timeout to the UDP socket so that it stops listening
                # after 2 minutes of inactivity

                # Get the port number assigned by the OS and print to console
                UDPport = UDPsocket.getsockname()[1]
                UDPaddr = UDPsocket.getsockname()

                # Put the UDP port number in a message and send it to the client using TCP
                print("Sending UDP port number to client using TCP connection...")
                TCPclientsocket.sendall('gameport {}'.format(UDPport).encode())

                # Break from loop once needed info is received
                break

            active = False # game not active by default

            # Game (UDP) loop
            while True:
                try:
                    # receive on UDP port here
                    incoming, UDPclientaddr = UDPsocket.recvfrom(4096)
                    
                    # print message
                    # print('Message received: {}'.format(incoming))
                    
                    if incoming.startswith(b'ready'):
                        # Game setup
                        active = True
                        word, word_blanks, attempts, win = gameSetup(argv)
                        print("Hidden Word: {}".format(word))
                        print("Starting game...")
                        message = b'instr '+INSTRUCTIONS.strip().encode()
                        UDPsocket.sendto(message, UDPclientaddr)
                        message = 'stat {} {}'.format(word_blanks, attempts).encode()
                        UDPsocket.sendto(message, UDPclientaddr)
                        
                    elif incoming.startswith(b'guess'):
                        guess = incoming[6:].decode()
                        word_blanks, attempts, win = checkGuess(word, word_blanks, attempts, guess, win)
                        # Losing conditions - break if end
                        if len(guess) > 1 and not win or attempts == 0:
                            # Handle lose conditions
                            message = b'end You lose.'
                            active = False
                        elif win:
                            # Handle win
                            message = b'end You win!'
                            active = False
                        else:
                            message = 'stat {} {}'.format(word_blanks, attempts).encode()
                        UDPsocket.sendto(message, UDPclientaddr)
                        
                    elif incoming.startswith(b'end'):
                        message = b'end The game was aborted!'
                        UDPsocket.sendto(message, UDPclientaddr)
                        
                    elif incoming.startswith(b'bye'):
                        UDPsocket.close()
                        TCPserversocket.close()
                        UDPsocket.sendto(b'bye', UDPclientaddr)
                        
                    
                except timeout: # catch UDP timeout
                    print("Ending game due to timeout...")
                    break # break and wait to accept another client


                #if ...:
                    # Game setup
                    # active = True
                    # word, word_blanks, attempts, win = gameSetup(argv)
                    # print("Hidden Word: {}".format(word))
                    # print("Starting game...")

                    # Send inst then stat messages


                #elif ...:

                    #word_blanks, attempts, win = checkGuess(word, word_blanks, attempts, guess, win)

                #   # Losing conditions - break if end
                #   if len(guess) > 1 and not win or attempts == 0 or win:
                #     # Handle win/lose conditions
                #     active = False
                #   else:


                # always send a response message to the client


            # end of UDP Game loop
            # close the TCP socket the client was using as well as the udp socket.


        # end of TCP loop

    except KeyboardInterrupt:

        # Close sockets
        print("Closing TCP and UDP sockets...")
        UDPsocket.close()
        TCPserversocket.close()

    ###########################################

if __name__ == "__main__":
    main()