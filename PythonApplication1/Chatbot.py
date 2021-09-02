def F_MAIN():
    # macht die Begrüßung und die erste Abfrage beim User
    F_INTRO()
    #
    F_THEMEN_ABFRAGE()
    
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
        for current_list_position in list_themenbereiche:

          # beide Variablen klein schreiben, um sie case sensitive vergleichen zu können ( BITTE != bitte )
          current_list_position = current_list_position.lower()
          user_input_lower = user_input.lower()

          if user_input_lower == current_list_position:
            hit = True
            break
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

    print("THEMEN:")
    print(user_input)
    
    #newTicket = ticket("Brian Lemke", "brian.lemke@mail.de", "017777777777", "10-12", "Hallo meine Maus geht nicht mehr. Ich brauch bitte eine neue Maus, danke!")
    
F_MAIN()
