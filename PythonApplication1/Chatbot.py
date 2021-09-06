# Imports
import sys
import mariadb

# Main Method, which controll everthing
def F_MAIN():
    # macht die Begrüßung und die erste Abfrage beim User
    F_INTRO()

    # fragt nach dem groben Themen Bereich
    F_THEMEN_ABFRAGE()

    # erstellt den Datenbank Connect
    F_DB_CONNECT()

    # sucht nach dem Themen
    F_FIND_SOLUTION()

    # holt sich die Ticket Informationen vom User
    F_TICKET_INFOS()

    # beendet den Chatbot
    F_EXIT()


list_themenbereiche = [ "Technische Störung", "Fragen zu Dienstleistungen", "Änderungen im Zusammenhang mit einer Software", "Sonstige Probleme" ]


def F_INTRO():
    print("Hallo und Wilkommen bei der Soulutions IT")
    print("Sie haben ein Problem, bei welchem Sie Hilfe benötigen?")
    print("")
    print("Bitte wählen Sie ein Stichwort aus, welches Ihr Problem am besten beschreibt.")
    print("Folgende Themenbereiche stehen zur Auswahl:")

    # Variable für unsere for Schleife
    counter = 1

    # vgl. for i in 1 2 3 4:
    for current_list_position in list_themenbereiche:
      print(f"\t {counter}. {current_list_position}")

      # counter+=1 => counter = counter + 1
      counter+=1

    print("")
    

def F_THEMEN_ABFRAGE():
    global user_input_themenbereich_nr
    user_input_themenbereich_nr = ""
    user_input_themenbereich = ""
    hit = False
    error_counter = 0
    
    while user_input_themenbereich == "":
    
      user_input_themenbereich = input("Bitte wählen Sie eine Themenbereich aus: ")

      #prüfen, ob die Eingabe valide war
      counter = 1
      while counter <= len(list_themenbereiche):
        
        # str(counter) => wir müssen 2 strings miteinander vergleichen
        if user_input_themenbereich == str(counter):
          hit = True
          # Setzen von user_input_themenbereich auf den entsprechenden String
          user_input_themenbereich = list_themenbereiche[counter-1]
          user_input_themenbereich_nr = counter
          break
        
        counter+=1
      
      if hit != True:
        counter = 1
        for current_list_position in list_themenbereiche:

          # beide Variablen klein schreiben, um sie case sensitive vergleichen zu können ( BITTE != bitte )
          current_list_position = current_list_position.lower()
          user_input_themenbereich_lower = user_input_themenbereich.lower()
          
          if user_input_themenbereich_lower == current_list_position:
            hit = True
            # Setzen von user_input_themenbereich auf den entsprechenden String
            user_input_themenbereich = list_themenbereiche[counter-1]
            user_input_themenbereich_nr = counter
            break
          counter+=1
      else:
        break

      # Wenn wir keinen Treffen hatten, Eingabe zurücksetzen    
      if hit == False:
        print("Ihre Eingabe war Fehlerhaft!")
        error_counter+=1
        user_input_themenbereich = ""

      if error_counter > 3:
        print("Sie haben mehrfach Fehlerhafte Eingaben getätigt! Bitte versuchen Sie es später erneut.")
        sys.exit(1)

    print("")
    print("Ihre Eingabe war:", user_input_themenbereich)

def F_FIND_SOLUTION():
    print("")
    print("Sie können diesen Bereich jederzeit mit dem Befehl \"!bye\" verlassen")

    user_input_problem = ""

    while user_input_problem == "":
        user_input_problem = input("Bitte geben sie Ihre Frage ein: ")

        if user_input_problem == "!bye":
            F_EXIT()
        if user_input_problem == "!TS":
            F_TICKET_SEARCH()
            user_input_problem = ""

        if user_input_themenbereich_nr != "4":

            try:
                # komisches Verhalten von MariaDB
                #cur.execute("Select ProblemKeyword, ProblemSolution from problems where ProblemCategoryID=? and ProblemKeyword like '%?%' ", (user_input_themenbereich_nr, user_input_problem))
                #cur.execute("Select ProblemKeyword, ProblemSolution from problems where ProblemCategoryID=? ", (user_input_themenbereich_nr, ))
                #cur.execute("Select ProblemKeyword, ProblemSolution from problems where ProblemKeyword LIKE \"?\" ", (test))

                # string manipulation => damit wir %-Zeichen in unserem Such String haben
                user_input_problem_man =  user_input_problem.replace(" ", "%")
                user_input_problem_man = "%" + user_input_problem_man + "%"

                statement = "Select ProblemKeyword, ProblemSolution from problems where ProblemCategoryID=? and ProblemKeyword LIKE ?"
                data = (user_input_themenbereich_nr, user_input_problem_man)
                cur.execute(statement, data)


            except mariadb.Error as e:
                print(f"Error: {e}")
                sys.exit(1)

            for (ProblemKeyword, ProblemSolution) in cur:
                print("")
                print(f"Problem-Beschreibung: {ProblemKeyword}")
                print(f"Problem-Lösung:       {ProblemSolution}")

                checker = "error"

                while checker == "error":
                    checker = input("Hat diese Antwort Ihr Problem gelöst? [j/n] ")

                    if checker != "j" && checker != "J" && checker != "n" && checker != "N":
                        checker = "error"
                    elif checker == "J" || checker == "j":
                        F_EXIT()


        else:
            print("XXX")


def F_TICKET_SEARCH():
    
    user_input_ticketnumber = ""

    while user_input_ticketnumber == "":
        user_input_ticketnumber = input("Bitte geben Sie ihre Ticket-Nummer ein: ")

        if user_input_ticketnumber.isdigit() == False:
            user_input_ticketnumber = ""

    # sucht in der DB nach der eingegebenen Ticket Nummer
    try:
        cur.execute("Select TicketNumber, TicketStatus from tickets where TicketNumber=?", (user_input_ticketnumber,))
    except mariadb.Error as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    for (TicketNumber, TicketStatus) in cur:
        print(f"Ticket-Nummer: {TicketNumber}")
        print(f"Ticket-Status: {TicketStatus}")


def F_TICKET_INFOS():
    user_name = ""
    user_email = ""
    user_number = ""
    user_availability = ""
    user_describtion = ""
    
    print("")  
    print("Wir benötigen noch ein paar Informationen für die Erstellung des Tickets")

    #User-Name Abfrage und Prüfung
    while user_name == "":

        # \t => Einrückungen
        user_name = input("Ihren Namen: \t \t \t")

        if user_name == "":
            print("Sie haben kein Namen eingegeben!")

        if F_CHECK_FOR_DIGITS(user_name) == True:
            print("Der Name enthält Zahlen!")
            user_name = ""
  
    #User-Email Abfrage und Prüfung
    while user_email == "":

        user_email = input("Ihre E-Mail-Adresse: \t \t")

        if user_email == "":
            print("Sie haben keine E-Mail-Adresse angegeben!")

        if "@" not in user_email:
            print("Die E-Mail-Adresse ist nicht gültig!")
            user_email = ""


    #User-Nummer Abfrage und Prüfung
    while user_number == "":

        user_number = input("Ihre Telefonnummer: \t \t")

        if user_number == "":
            print("Sie haben keine Nummer eingegeben!")

        if user_number.isdigit() == False:
            print("Die Nummer darf nur Zahlen enthalten!")
            user_number = ""
  

    #User-Verfügbarkeit Abfrage und Prüfung
    while user_availability == "":

        user_availability = input("Ihre Erreichbarkeit: \t \t")

        if user_availability == "":
            print("Sie haben keine Erreichbarkeit eingegeben!")


    #User-Fehlerbeschreibung Abfrage und Prüfung
    while user_describtion == "":

        user_describtion = input("Ihre Fehlerbeschreibung: \t")

        if user_describtion == "":
            print("Sie haben keine Fehlerbeschreibung eingegeben!")


    #F_WRITE_TO_DATABASE(user_name, user_email, user_number, user_availability, user_describtion)

    print("Ein Mitarbeiter wird sich so schnell wie möglich um Ihre Anfrage kümmern.")
    print("")


def F_CHECK_FOR_DIGITS(inputString):
  return any(current_char.isdigit() for current_char in inputString)


def F_WRITE_TO_DATABASE(UserName, UserEmail, UserTelephonenumber, UserAvailability, UserDescribtion):
    
    try:
        cur.execute("Insert into tickets (UserName, UserEmail, UserTelephonenumber, UserAvailability, UserDescribtion) values (?, ?, ?, ?, ?)" , (UserName, UserEmail, UserTelephonenumber, UserAvailability, UserDescribtion) )
    except mariadb.Error as e:
        print(f"Error: {e}")
        sys.exit(1)


    conn.commit()

    print("")
    print("Ich Ticket wurde unter folgender Ticket-Nummer erstellt.")
    print(f"Ticket-Nummer: {cur.lastrowid}")
    print("")

    #cur.execute("Select TicketNumber, UserName from tickets where creationdate like '' ")
    #for (TicketNumber, UserName) in cur:
        
        #print(f"Ticket Nummer: {TicketNumber}")

def F_DB_CONNECT():
  # Connect to MariaDB Platform
    try:
        global conn
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="chatbot"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    global cur 
    cur = conn.cursor()

def F_EXIT():
    conn.close()
    print("Wir wünschen Ihnen noch einen schönen Tag.")
    sys.exit(1)


F_MAIN()
