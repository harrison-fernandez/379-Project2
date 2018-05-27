# 379-Project2

Members:

* Erick Jean Reyes
* Harrison Fernandez

Responsibilities:

* Client.py written by Harrison Fernandez
* Server.py written by Erick Jean Reyes

Comments:
Run the server program first, writing in the terminal: "python3 server.py (word to play in hangman game)"
Server will tell you the port number, then the client can enter "python3 client.py (server name, can be "localhost" if needed) (port number)"
Client will be asked to enter their name (enter 'start'), and type "start" again to start the game. They will receive instructions. 
The client will have to enter "guess 'char'" to guess a letter or "guess 'word'" to try to solve the puzzle. If the guessed word does not match, the game will end. Clients can also type "quit" or "end" to stop playing.
