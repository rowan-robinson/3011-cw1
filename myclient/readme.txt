# MODULE-LEADER-RATING-BOARD
for COMP3011 - CW1
by Rowan Robinson
(201658374, sc22r2r@leeds.ac.uk)

==========================================================================

This is a web app featuring a server application and a client application.
To use it, run the client application named client.py

From there, follow the instructions to get the most out of the client app.
For convenience, below is a list of all possible actions.

==========================================================================

help
• Displays this command list

register
• Register as a new user

login
• Log in with your credentials
• REQUIRED ARGUMENTS: url
  - url:          the address of the professor rating service

logout
• Log out of your session

list
• Displays a list of all module instances

view
• Displays the average rating of all professors

average
• Displays the average rating of a specific professor for a certain module
• REQUIRED ARGUMENTS: professor_id module_code
  - professor_id: the ID of the professor
  - module_code:  the code of the module

rate
• Lets you give a rating of a professor for a certain module instance
• REQUIRED ARGUMENTS: professor_id module_code year semester rating
  - professor_id: the ID of the professor
  - module_code:  the code of the module
  - year:         the academic year the module was taught in
  - semester:     the semester the module was taught in
  - rating:       your score from 1 - 5

quit
• Quits this client program

==========================================================================

The client program has two domain options, one local and one for pythonanywhere:

• http://127.0.0.1:8000/
• https://sc22r2r.pythonanywhere.com/

The default is the latter, and you can switch to the former by commenting out line 4,
and uncommenting line 5

==========================================================================

The database comes with an admin user, whose credentials are:

username: admin
email: admin@3011.com
password: p (yes, just a single character... not very secure but quicker when testing!)

Alongside this are some pre-existing modules, professors, module instances, and a rating.

==========================================================================

Please `pip install requirements.txt` to make sure everything is functional!

==========================================================================

Enjoy rating your favourite professors!