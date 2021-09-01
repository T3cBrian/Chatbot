def F_MAIN():
    F_INTRO()
    F_THEMEN()
    
user_input = ""

def F_INTRO():
    print("Hallo und Wilkommen bei der IT Soulution")
    print("Sie haben ein Problem, bei welchem Sie Hilfe benötigen?")
    print("Bitte wählen Sie ein Stichwort aus, welches Ihr Problem am besten beschreibt.")
    print("Folgende Themenbereiche stehen zur Auswahl:")
    print("")

    global user_input

    user_input = input("Hier tippen")

    print("Hallo")
    print("Ihre Eingabe war:", user_input)

    

def F_THEMEN():
    print("THEMEN:")
    print(user_input)
    
    newTicket = ticket("Brian Lemke", "brian.lemke@mail.de", "017777777777", "10-12", "Hallo meine Maus geht nicht mehr. Ich brauch bitte eine neue Maus, danke!")
    
F_MAIN()