# IMPORTS
import requests

root = "https://rowanrobinson.pythonanywhere.com/"
# root = "http://127.0.0.1:8000/"
session = requests.Session()


# FUNCTION: help()
# provides help to the user in the form of a command list
def help():
    print("\n- -AVAILABLE COMMANDS - -\n")
    # help
    print("\nhelp")
    print("• Displays this command list")
    # register
    print("\nregister")
    print("• Register as a new user")
    # login
    print("\nlogin")
    print("• Log in with your credentials")
    print("• REQUIRED ARGUMENTS: url")
    print("  - url:          the address of the professor rating service")
    # logout
    print("\nlogout")
    print("• Log out of your session")
    # list
    print("\nlist")
    print("• Displays a list of all module instances")
    # view
    print("\nview")
    print("• Displays the average rating of all professors")
    # average
    print("\naverage")
    print("• Displays the average rating of a specific professor for a certain module")
    print("• REQUIRED ARGUMENTS: professor_id module_code")
    print("  - professor_id: the ID of the professor")
    print("  - module_code:  the code of the module")
    # rate
    print("\nrate")
    print("• Lets you give a rating of a professor for a certain module instance")
    print("• REQUIRED ARGUMENTS: professor_id module_code year semester rating")
    print("  - professor_id: the ID of the professor")
    print("  - module_code:  the code of the module")
    print("  - year:         the academic year the module was taught in")
    print("  - semester:     the semester the module was taught in")
    print("  - rating:       your score from 1 - 5")
    # quit
    print("\nquit")
    print("• Quits this client program")

# FUNCTION: register()
# registers a new user
def register():
    print("- REGISTER -")
    print("")

    # get input from the user and package this as a payload
    username = input("Enter your username: ")
    email    = input("Enter your email: ")
    password = input("Enter your password: ")
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    # pass the payload to the server to register the user
    try:
        response = session.post(root + "/users/", json=payload)

        if response.status_code == 200:
            print("\n- - = REGISTERED! - -")
        else:
            print("\nCould not register.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: login()
# lets the user log in
def login(argList):
    # ensure the user has provided a url to login at
    if len(argList) != 1:
        print("Missing or too many arguments!")
        print("\nCORRECT FORM:")
        print("   login url")
        print("(use \'help\' for more details!)")
        return
    
    print("- LOGIN -")
    print("- logging in at " + str(argList[0]))
    print("")

    # get input from the user and package this as a payload
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    payload = {
        "username": username,
        "password": password
    }
    # pass the payload to the server to authenticate the user details
    try:
        response = session.post(root + "/user-login", json=payload)

        if response.status_code == 200:
            print("\n- - = LOGGED IN! = - -")
            token = response.json()["token"]
            session.headers.update({'Authorization': ("Token " + token)})
        else:
            print("\nCould not log in.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: logout()
# logs the user out of their session
def logout():
    try:
        response = session.post(f'{root}/user-logout')

        if response.status_code == 200:
            print("\n- - = LOGGED OUT = - -")
            session.headers.pop("Authorization", None)
            session.cookies.clear()
        else:
            print("\nCould not log out.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: list()
# lists all module instances
def list():
    try:
        response  = session.get(f'{root}/moduleinstances/')
        # required for foreign keys
        responseMod = session.get(f'{root}/modules/')
        responsePro = session.get(f'{root}/professors/')

        if response.status_code == 200:
            print("\n- MODULE INSTANCE LIST -\n")
            print("| code | name                 | year | semester | taught by")
            print("| - - -|- - - - - - - - - - - | - - -|- - - - - | - - - - -")

            theResults = response.json()["results"]
            for x in range(0, response.json()["count"]):
                # print results up to the first prof...
                print(
                    "| " + 
                    # using generator expressions for effeciency
                    str((next(i for i in responseMod.json()["results"] if i["code"] == theResults[x]["code"])["code"])).ljust(4) + " | " + 
                    str((next(i for i in responseMod.json()["results"] if i["code"] == theResults[x]["code"])["name"])).ljust(20) + " | " + 
                    str(theResults[x]["year"]).ljust(4) + " | " + 
                    str(theResults[x]["semester"]).ljust(8) + " | " + 
                    str((next(i for i in responsePro.json()["results"] if i["code"] == theResults[x]["leaders"][0])["code"])) + " - " + 
                    str((next(i for i in responsePro.json()["results"] if i["code"] == theResults[x]["leaders"][0])["name"]))
                )
                # ...then print the rest of professors the module instance was/is taught by if there are more than 1 prof.
                for y in range(1, len(theResults[x]["leaders"])):
                    print(
                        (" " * 50) +
                        str((next(i for i in responsePro.json()["results"] if i["code"] == theResults[x]["leaders"][y])["code"])) + " - " + 
                        str((next(i for i in responsePro.json()["results"] if i["code"] == theResults[x]["leaders"][y])["name"]))
                    )
        else:
            print("Could not collect module instances.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: view()
# displays ratings of all professors
def view():
    try:
        response  = session.get(f'{root}/professors/')
        # required for foreign keys
        responseRat = session.get(f'{root}/ratings/')

        if response.status_code == 200:
            print("\n- PROFESSOR RATINGS LIST -\n")
            # header
            print("| code | name                 | avg. rating")
            print("| - - -|- - - - - - - - - - - | - - - - - -")

            theResults = response.json()["results"]
            for x in range(0, response.json()["count"]):
                # before printing anything, calculate the average rating that the professor
                # received across all module instances they taught
                allRatings = []
                avgProfRating = -1
                for y in range(0, responseRat.json()["count"]):
                    if responseRat.json()["results"][y]["professor"] == theResults[x]["code"]:
                        allRatings.append(responseRat.json()["results"][y]["score"])
                if len(allRatings) > 0:
                    totalRating = 0
                    for z in range(0, len(allRatings)):
                        totalRating += allRatings[z]
                    avgProfRating = round(totalRating / len(allRatings))

                # print results, accounting for if a professor has received no ratings
                if avgProfRating == 0:
                    print(
                        "| " + 
                        str(theResults[x]["code"]).ljust(4) + " | " + 
                        str(theResults[x]["name"]).ljust(20) + " | " + 
                        str("N/A")
                    )
                else:
                    print(
                        "| " + 
                        str(theResults[x]["code"]).ljust(4) + " | " + 
                        str(theResults[x]["name"]).ljust(20) + " | " + 
                        str("*" * avgProfRating)
                    )
        else:
            print("Could not collect professors and their ratings.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: average()
# displays average rating of specific professor for certain module
def average(argList):
    # ensure the user has provided all of the appropriate arguments
    if len(argList) != 2:
        print("Missing or too many arguments!")
        print("\nCORRECT FORM:")
        print("   average professor_id module_code")
        print("(use \'help\' for more details!)")
        return
    
    try:
        response = session.get(f'{root}/professors-avg/{argList[0]}/{argList[1]}/')

        if response.status_code == 200:
            print("\n- AVG PROFESSOR RATING FOR MODULE -\n")
            theResponse = response.json()
            if theResponse["avg-rating"] == -1:
                print("The professor " + 
                    theResponse["professor-name"] + " (" + theResponse["professor-code"] + ") has received no ratings for the module " + 
                    theResponse["module-name"] + " (" + theResponse["module-code"] + ")"
                )
            else:
                print("The average rating of " + 
                    theResponse["professor-name"] + " (" + theResponse["professor-code"] + ") for the module " + 
                    theResponse["module-name"] + " (" + theResponse["module-code"] + ") is " +
                    ("*" * theResponse["avg-rating"])
                )
        else:
            print("Could not collect average professor rating.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

# FUNCTION: rate()
# lets user rate professor for certain module instance
def rate(argList):
    # ensure the user has provided all of the appropriate arguments
    if len(argList) != 5:
        print("Missing or too many arguments!")
        print("\nCORRECT FORM:")
        print("   rate professor_id module_code year semester rating")
        print("(use \'help\' for more details!)")
        return
    
    print("- RATING -")
    print("- rating " + str(argList[0]) + " for the module " + str(argList[1]) + " for " + str(argList[2]) + ", sem. " + str(argList[3]) + " a rating of " + str(argList[4]))
    print("")

    try:
        payload = {
            'professor': argList[0],
            'module': argList[1],
            'year': int(argList[2]),
            'semester': int(argList[3]),
            'rating': int(argList[4])
        }
        print(payload)
        response = session.post(f'{root}/ratings/', json=payload)
        print("hi")
        if response.status_code == 201:
            print("\n- - = RATED SUCCESSEFULLY! = - -")
        else:
            print("Could not submit rating.")
            print(response.json())
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")


# FUNCTION: main()
# core functionality
def main():
    print("")
    print(". . . : : : : : : : : : : : : : : : : : : : : : . . .")
    print("- = ≡ WELCOME TO THE MODULE-LEADER-RATING-BOARD ≡ = -")
    print(". . . : : : : : : : : : : : : : : : : : : : : : . . .")
    print("")

    # main loop of the client program
    while True:
        print("= = = = = = = = = = = =")

        # get input from the user to see what command they want to perform
        # and any arguments if there are any
        userInput = input("Choose a command (use \'help\' for command list): ").split(" ")
        # split input into command and arguments
        command = userInput[0]
        args = []
        if len(userInput) > 1:
            for x in range(1, len(userInput)):
                args.append(userInput[x])

        # handle user input
        if command == "help":
            help()
        elif command == "register":
            register()
        elif command == "login":
            login(args)
        elif command == "logout":
            logout()
        elif command == "list":
            list()
        elif command == "view":
            view()
        elif command == "average":
            average(args)
        elif command == "rate":
            rate(args)
        elif command == "quit":
            break
        else:
            print("Invalid command, please try again.")

        print("")

if __name__ == "__main__":
    main()