# Imports
import sys
import mariadb
from datetime import date


# Main Method, wich controll everthing
def F_MAIN():
    # macht die Begrüßung und die erste Abfrage beim User
    F_INTRO()
    #
    #F_THEMEN_ABFRAGE()
    #F_TICKET_INFOS()
    F_WRITE_TO_DATABASE()


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
      # {}. {}".format(x ,y) => formatiert die Ausgabe, da wir andernfalls Leerzeichen nach den Variablen haben
      print("\t {}. {}".format(counter, current_list_position) )

      # counter+=1 => counter = counter + 1
      counter+=1

    print("")
    

def F_THEMEN_ABFRAGE():
    user_input = ""
    hit = False
    error_counter = 0
    
    while user_input == "":
    
      user_input = input("Bitte wählen Sie eine Themenbereich aus: ")

      #prüfen, ob die Eingabe valide war
      counter = 1
      while counter <= len(list_themenbereiche):
        
        # str(counter) => wir müssen 2 strings miteinander vergleichen
        if user_input == str(counter):
          hit = True
          # Setzen von user_input auf den entsprechenden String
          user_input = list_themenbereiche[counter-1]
          break
        
        counter+=1
      
      if hit != True:
        counter = 1
        for current_list_position in list_themenbereiche:

          # beide Variablen klein schreiben, um sie case sensitive vergleichen zu können ( BITTE != bitte )
          current_list_position = current_list_position.lower()
          user_input_lower = user_input.lower()
          
          if user_input_lower == current_list_position:
            hit = True
            # Setzen von user_input auf den entsprechenden String
            user_input = list_themenbereiche[counter-1]
            break
          counter+=1
      else:
        break

      # Wenn wir keinen Treffen hatten, Eingabe zurücksetzen    
      if hit == False:
        print("Ihre Eingabe war Fehlerhaft!")
        error_counter+=1
        user_input = ""

      if error_counter > 3:
        print("Sie haben mehrfach Fehlerhafte Eingaben getätigt! Bitte versuchen Sie es später erneut.")
        exit()

    print("")
    print("Ihre Eingabe war:", user_input)
    
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
    user_name = input("Ihren Namen: \t \t \t \t")

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


  #newTicket = ticket( user_name, user_email, user_number, user_availability, user_describtion)

  print("Ihr Ticket wurde aufgenommen. Ein Mitarbeiter wird sich so schnell wie möglich um Ihre Anfrage kümmern.")


def F_CHECK_FOR_DIGITS(inputString):
  return any(current_char.isdigit() for current_char in inputString)


def F_WRITE_TO_DATABASE():
    print("Ticket wird erstellt.")

    # Connect to MariaDB Platform
    try:
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
    cur = conn.cursor()

    cur.execute("Insert into tickets (UserName, UserEmail, UserTelephonenumber, UserAvailibility, UserDescribtion) values #(user_name, user_email, user_number, user_availability, user_describtion)")

    today = date.today()

    print(today)

    cur.execute("Select TicketNumber, UserName from tickets where creationdate like '' ")
    for (TicketNumber, UserName) in cur:
        print("Ich Ticket wurde unter folgender Ticketnummer erstellt.")
        print(f"Ticket Nummer: {TicketNumber}")

F_MAIN()


# Objekt vom Typ Ticket erstellen => just for fun
#newTicket = ticket("Brian Lemke", "brian.lemke@mail.de", "017777777777", "10-12", "Hallo meine Maus geht nicht mehr. Ich brauch bitte eine neue Maus, danke!")
