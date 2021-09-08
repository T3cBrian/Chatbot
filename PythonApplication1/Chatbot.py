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
    print("Sie können diesen Bereich jederzeit mit dem Befehl \"!bye\" verlassen oder mit dem Befehl \"!restart\" den Themenbereich neu auswählen.")
    print("Bitte geben Sie ein Stichwort ein, welches Ihre Frage/ Ihr Problem am besten beschreibt")
    print("")

    user_input_problem = ""

    while user_input_problem == "":
        user_input_problem = input("Ihre Frage/ Ihr Problem: ")

        if user_input_problem == "!bye":
            F_EXIT()
            break
        if user_input_problem == "!TS":
            F_TICKET_SEARCH()
            user_input_problem = ""
            continue
        if user_input_problem == "!restart":
            F_THEMEN_ABFRAGE()
            user_input_problem = ""
            continue


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

        # der checker wird im folgenden benutzt um mehrer Sachen zu testen, zum einen ob wir überhaupt etwas in der DB gefunden haben, später dann wie unsere Antwort war und wie wir weiter machen möchten
        checker = "initialize"

        for (ProblemKeyword, ProblemSolution) in cur:
            print("")
            print(f"Problem-Beschreibung: {ProblemKeyword}")
            print(f"Problem-Lösung:       {ProblemSolution}")

            checker = "error"

            while checker == "error":
                checker = input("Hat diese Antwort Ihr Problem gelöst? [j/n]: ")

                checker = checker.lower()

                if checker == "j" or checker == "ja":
                    checker = "break"
                    break
                elif checker == "!bye":
                    F_EXIT()
                elif checker == "!ts":
                    F_TICKET_SEARCH()
                    checker = "break"
                    break
                elif checker != "j" and checker != "ja" and checker != "n" and checker != "nein":
                    checker = "error"

            if checker == "break":
                user_input_problem = ""
                break
        
        checker_no_solution = False

        # Wenn der Checker n o. N ist haben wir noch keine Lösung gefunden
        if checker == "n" or checker == "nein":
            print("")
            print("Leider hat keiner unserer Vorschläge eine Lösung erziehlt.")
            checker_no_solution = True
                
        #wenn das true ist, dann hatten wir keine Attribute im Objekt "cur"
        elif checker == "initialize":
            print("")
            print("Leider konnten wir keine Problembeschreibung zu Ihrem eingegebenem Stichwort finden.")
            checker_no_solution = True

        if checker_no_solution == True:
            print("Bitte probieren Sie es doch mit einem anderen Stichwort oder etwas allgemeiner. -- 1")
            print("Sie können auch gerne direkt ein Ticket erstellen                               -- 2")
            print("")

            user_input_no_object = ""

            while user_input_no_object == "":

                user_input_no_object = input("Wie möchten sie fortfahren? [1/2]: ")

                if user_input_no_object == "":
                    print("Bitte antworten Sie mit 1 oder 2")
                    continue

                if user_input_no_object == "1":
                    # wir setzen die Frage zurück und starten somit mit einer neuen Abfrage, da wir immernoch in der while schleife sind
                    user_input_problem = ""
                    continue
                elif user_input_no_object == "2":
                    # springen direkt in die Function um ein Ticket zu erstellen und danach beenden wir den chatbot
                    F_TICKET_INFOS()
                    F_EXIT()
                else:
                    user_input_problem = ""
                    print("Bitte antworten Sie mit 1 oder 2")
                    continue


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
        
    checker_for_tricket = False

    for (TicketNumber, TicketStatus) in cur:
        print(f"Ticket-Nummer: {TicketNumber}")
        print(f"Ticket-Status: {TicketStatus}")
        checker_for_tricket = True

    if checker_for_tricket == False:
        print("Es gibt leider kein Ticket zu der eingegebenen Ticket-Nummer")


def F_TICKET_INFOS():
    user_name = ""
    user_email = ""
    user_number = ""
    user_availability = ""
    user_describtion = ""
    
    print("")  
    print("Um ein Ticket zu erstellen, füllen Sie bitte folgende Informationen aus.")

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


    F_WRITE_TO_DATABASE(user_name, user_email, user_number, user_availability, user_describtion)

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
            password="",
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
    input("Press Enter to exit")
    sys.exit(1)


F_MAIN()
