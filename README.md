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

Sample Server Interface: 
harrison@harrison:~/Downloads/project2/src$ python3 server.py hangman
Server is running...
Creating TCP socket...
Server is listening on port 51215
Waiting for a client...
Creating UDP socket...
Sending UDP port number to client using TCP connection...
Hidden Word: hangman
Starting game...
Correctly guessed char
Attempts left: 5
Win status: False
Correctly guessed char
Attempts left: 5
Win status: False
Guess was more than 1 char - win/lose only
Win status: 1


Sample Client Interface:
harrison@harrison:~/Downloads/project2/src$ python3 client.py localhost 51215
Client is running...
Remote host: localhost, remote TCP port: 51215
Please enter your name: start
The server address is localhost:51215
Received UDP port#: 55677
('localhost', 55677)
>start
This is hangman. You will guess one letter at a time. If the letter is in
the hidden word, the "-" will be replaced by the correct letter. Guessing multiple letters at
a time will be considered as guessing the entire word (which will result in either a win
or loss automatically - win if correct, loss if incorrect). You win if you either guess all of
the correct letters or guess the word correctly. You lose if you run out of attempts. Attempts
will be decremented in the case of an incorrect or repeated letter guess.
Word: ------- Attempts left: 5
>h
>guess h
Word: h------ Attempts left: 5
>guess a
Word: ha---a- Attempts left: 5
>guess hangman
You win!
>
