import sqlite3
import pandas as pd
from datetime import datetime
from tabulate import tabulate

#connects to database
con = sqlite3.connect("main.db")
  #used to execute SQLite queries
cur = con.cursor()
#used to toggle foreign key constrains on / off
cur.execute("PRAGMA foreign_keys = OFF")
#all DFs will be printed with all table columns
pd.options.display.max_columns = None


def login():
  try:
    userUsername = input("username: ")
    userPassword = input("password: ")
    #defines attemptLogin query
    attemptLogin = (
        "SELECT * FROM user_table WHERE user_username = ? AND user_password = ?")
    #executes attemptLogin query
    cur.execute(attemptLogin,
                [userUsername, userPassword])  # executes the login function
    #fetches result of query
    currentUser = cur.fetchall()
    if currentUser:
      #successful login attempt
      print("\nSuccessful login.")
      mainMenu()
    else:
      #unsuccessful login attempt, prompts user to try again
      print("\nUnsuccessful login attempt, please try again.")
      login()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nUnsuccessful login attempt, please try again.")
    login()

def register():
  try:
    print("You have selected register")
    newUserUsername = input("username: ")
    newUserPassword = input("password: ")
    newUserLevel = int(input("level: "))
    #defines SQLite query
    createNewAccount = (
        "INSERT INTO user_table "
        "(user_username, user_password, user_level) VALUES (?,?,?)"
    )
    #executes SQLite query
    cur.execute(createNewAccount,
                [newUserUsername, newUserPassword, newUserLevel
                 ])
    #commits changes
    con.commit()
    print("\nAccount created successfully, "
    "press any key to return to the login/register menu.")
    try:
      returnSelection = int(input())
      if returnSelection == 1:
        loginRegisterMenu()
      else:
        print("\nReturning to login/register menu.")
        print("\n")
        loginRegisterMenu()
        #catches any errors (e.g., symbol or int entered)
    except ValueError:
      #catches any errors (e.g., symbol or int entered)
      #invalid selection, prompts user to try again
      print("\nReturning to login/register menu.")
      print("\n")
      loginRegisterMenu()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nUnsuccessful registration attempt, please try again.")
    register()

def loginRegisterMenu():
  #displays a header for login/register menu
  print(' Login/Register Menu '.center(50, '-'))
  #displays login/register menu choices
  print("1) Login")
  print("2) Register")
  print("3) bypass (for testing)")
  print(''.center(50, '-'))
  #displays a footer for login/register menu
  try:
    print("\n")
    #prompts the user to make a menu selection
    loginRegisterSelection = int(
        input("Please select an option from the menu: "))
    print("\n")
    #checks user's input, proceeds to chosen function
    if loginRegisterSelection == 1:
      login()
    if loginRegisterSelection == 2:
      register()
    if loginRegisterSelection == 3:
      mainMenu()
    if loginRegisterSelection == 4:
      execute_sql_command(con, cur)
    else:
      #invalid selection, prompts user to try again
      print("\nInvalid option selected, please try again.")
      loginRegisterMenu()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nInvalid option selected, please try again.")
    loginRegisterMenu()

import sqlite3

def execute_sql_command(con, cur):
    try:
        cur.execute("""
        """)
        con.commit()
        print("Command executed successfully.")
    except sqlite3.Error as e:
        print("Error executing command", e)

def returnMenu():
  #displays return menu choices
  print("\nPress '1' to return to the main menu")
  print("\nPress any other key to logout")
  try:
    returnSelection = int(input())
    #checks user's input, proceeds to chosen function
    if returnSelection == 1:
      mainMenu()
    else:
      print("\nlogging out")
      loginRegisterMenu()
  #catches any errors (e.g., symbol or int entered)
  #invalid selection, prompts user to try again
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, logs user out
    print("\nlogging out")
    loginRegisterMenu()

def mainMenu():
  #displays a header for login/register menu
  print(' Main Menu '.center(50, '-'))
  #displays main menu choices
  print("1) View Tables")
  print("2) Create Table entry")
  print("3) Modify Table entry")
  print("4) Delete Table entry")
  print("5) View Statistics")
  print("6) Sign Out")
  print(''.center(50, '-'))
  #displays a footer for login/register menu
  try:
    print("\n")
    #prompts the user to make a menu selection
    mainMenuSelection = int(input("Please select an option from the menu: "))
    print("\n")
    #checks user's input, proceeds to chosen function
    if mainMenuSelection == 1:
      viewTableMenu()
    elif mainMenuSelection == 2:
      insertTableDataMenu()
    elif mainMenuSelection == 3:
      modifyTableDataMenu()
    elif mainMenuSelection == 4:
      deleteTableDataMenu()
    elif mainMenuSelection == 5:
      statQuery = '''SELECT strftime('%Y-%W', estimated_departure_datetime) 
      as week, COUNT(*) as num_flights FROM flight_table GROUP 
      BY week ORDER BY week;
      '''

      statDf = pd.read_sql_query(statQuery, con)
      print("Flights per week")
      print(tabulate(statDf,headers='keys',
         tablefmt='fancy_grid',showindex=False))
      returnMenu()
    elif mainMenuSelection == 6:
      print("\nSuccessful Sign Out")
      loginRegisterMenu()
    #catches invalid input (e.g., char or invalid int entered)
    #invalid selection, prompts user to try again
    else:
      print("\nInvalid option selected, Please try again")
      mainMenu()
  #catches any errors (e.g., symbol or char entered)
  #invalid selection, prompts user to try again
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nInvalid option selected, Please try again")
    mainMenu()

def manipulateTable(selectedTableName):
  #checks user's input, proceeds to chosen function
  if selectedTableName == "aircraft_table":
    try:
      print("\n")
      #prompts the user to enter a callsign
      aircraftCallsign = input("Please enter an aircraft callsign to "
                               "view all flights assigned to the aircraft: ")
      print("\n")
      #executes SQLite query
      cur.execute("SELECT * FROM aircraft_table WHERE aircraft_callsign = ?",
                  (aircraftCallsign, ))
      selectedAircraft = cur.fetchone()
      if selectedAircraft is None:
        #no aircraft associated with user input
        print("No aircraft is currently associated with that callsign")
      else:
        #aircraft associated with user input
        fetchAircraftFlights = (
            "SELECT * FROM flight_table WHERE aircraft_callsign = ?")
        #defines readable headers (instead of table keys)
        headers = [
            'ID', 'Callsign', 'Pilot ID', 'Co-pilot ID', 'Dep. Airport',
            'Dest. Airport', 'Departure DateTime', 'Arrival DateTime',
            'Duration', 'Passengers'
        ]
        #defines flightTableDf if there are entries in the table
        flightTableDf = pd.read_sql_query(fetchAircraftFlights,
                                          con,
                                          params=[aircraftCallsign])
        #prints message to user if table is empty
        if flightTableDf.empty:
          print("\nNo flights are currently assigned to this aircraft")
        else:
          #prints flightTableDf is a stylised format
          #uses readble headers (instead of table ekys)
          print(tabulate(flightTableDf,headers=headers,
                         tablefmt='fancy_grid',showindex=False))
          print("\n")
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    except ValueError:
      #catches any errors (e.g., symbol or int entered)
      #invalid selection, prompts user to try again
      print("\nInvalid option selected, Please try again")
      manipulateTable(selectedTableName)

  #checks user's input, proceeds to chosen function
  elif selectedTableName == "airport_table":
    try:
      #prompts the user to enter an airport ID
      airportId = input(
          "\nEnter the ID of the airport to see flights running to/from this location: "
      )
      #executes SQLite query
      cur.execute("SELECT * FROM airport_table WHERE airport_id=?",
                  (airportId, ))
      selectedAirport = cur.fetchone()
      if selectedAirport is None:
        #no aiport associated with user input
        print("No airport is associated with that ID.")
      else:
        #aiport associated with user input
        fetchAirport = (
            "SELECT * FROM flight_table WHERE departure_airport = ? OR arrival_airport = ?"
        )
        #defines airportTableDf if there are entries in the table
        airportTableDf = pd.read_sql_query(
            fetchAirport, con, params=[selectedAirport[1], selectedAirport[1]])

        if airportTableDf.empty:
          print("\nNo flights are currently running from/to this airport")
        else:
          #defines readable headers (instead of table keys)
          headers = [
              'ID', 'Aircraft Callsign', 'Pilot ID', 'Co-pilot ID',
              'Dep. Airport', 'Dest. Airport', 'Departure DateTime',
              'Arrival DateTime', 'Duration', 'Passengers'
          ]
          #prints flightTableDf is a stylised format
          #uses readble headers (instead of table ekys)
          print(tabulate(airportTableDf,headers=headers,
                         tablefmt='fancy_grid',showindex=False))

    except ValueError:
      #catches any errors (e.g., symbol or int entered)
      #invalid selection, prompts user to try again
      print("Invalid option selected. Please try again")
      manipulateTable(selectedTableName)

  #checks user's input, proceeds to chosen function
  elif selectedTableName == "pilot_table":
    try:
      #prompts the user to enter a pilot ID
      pilotId = input("\nEnter pilot ID to view associated flights: ")
      #executes SQLite query
      cur.execute("SELECT * FROM pilot_table WHERE pilot_id =?", (pilotId, ))
      selectedPilot = cur.fetchone()
      if selectedPilot is None:
        #no pilot associated with user input
        print("\nNo pilot is associated with that pilot ID")
      else:
        #pilot associated with user input
        fetchPilot = (
            "SELECT * FROM flight_table WHERE pilot1_id = ? OR pilot2_id = ?")
        #defines flightTableDf if there are entries in the table
        pilotTableDf = pd.read_sql_query(fetchPilot,
                                         con,
                                         params=[pilotId, pilotId])
        if pilotTableDf.empty:
          print("\nThis pilot isn't currently assigned to any flights")
        else:
          #defines readable headers (instead of table keys)
          headers = [
              'ID', 'Aircraft Callsign', 'Pilot ID', 'Co-pilot ID',
              'Dep. Airport', 'Dest. Airport', 'Departure DateTime',
              'Arrival DateTime', 'Duration', 'Passengers'
          ]
          #prints flightTableDf is a stylised format
          #uses readble headers (instead of table ekys)
          print(tabulate(pilotTableDf,headers=headers,
                       tablefmt='fancy_grid',showindex=False))

    except ValueError:
      #catches any errors (e.g., symbol or int entered)
      #invalid selection, prompts user to try again
      print("Invalid option selected, Please try again")
      manipulateTable(selectedTableName)

  else:
    #no other table selections use manipulateTable function
    returnMenu()

def viewTableMenu():
  try:
    #displays a header for menu
    print(' View Table Menu '.center(50, '-'))
    #displays menu choices
    validTables = {
        1: "flight_table",
        2: "aircraft_table",
        3: "pilot_table",
        4: "airport_table",
        5: "user_table",
    }
    #uses dictionary to set key(numerical identifier) value(table) pair
    for numericalIdentifier, databaseTable in validTables.items():
      print(f"{numericalIdentifier}) {databaseTable}")
    print("6) Return to main menu")
    #displays a footer for menu

    print(''.center(50, '-'))
    # Get the numerical choice from the user
    viewTableSelection = int(
        input("\nPlease select the table you would like to view: "))
    selectedTableName = validTables.get(viewTableSelection)

    if selectedTableName:
      print("\n")
      # tables are outputted as a dataframe to
      # maximize readability in tables with many columns
      tableDf = pd.read_sql_query(f"SELECT * FROM {selectedTableName}", con)
      if selectedTableName == "flight_table":
        headers = [
            'ID', 'Callsign', 'Pilot ID', 'Co-pilot ID', 'Dep. Airport',
            'Dest. Airport', 'Departure DateTime', 'Arrival DateTime',
            'Duration', 'Passengers'
        ]
        # if the table dataframe isn't empty it will be printed
        if not tableDf.empty:
          #prints flightTableDf is a stylised format
          print(tabulate(tableDf,headers=headers,
                         tablefmt='fancy_grid',showindex=False))
          # if the table dataframe IS empty
          # a message will be printed, rather than an empty dataframe
          manipulateTable(selectedTableName)
          returnMenu()
        else:
          print(f"The {selectedTableName} is currently empty.")
          returnMenu()
      else:
        # if the table dataframe isn't empty it will be printed
        if not tableDf.empty:
          #prints flightTableDf is a stylised format
          print(tabulate(tableDf,headers='keys',
                         tablefmt='fancy_grid',showindex=False))
          # if the table dataframe IS empty
          # a message will be printed, rather than an empty dataframe
          manipulateTable(selectedTableName)
          returnMenu()
        else:
          print(f"The {selectedTableName} is currently empty.")
          returnMenu()
    elif viewTableSelection == 5:
      mainMenu()
    else:
      print("\nInvalid option, please try again")
      viewTableMenu()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nInvalid option, please try again")
    returnMenu()


def insertTableDataMenu():
  try:
    #displays a header for menu
    print(' Create Table Entry Menu '.center(50, '-'))
    #displays menu choices
    validTables = {
        1: "flight_table",
        2: "aircraft_table",
        3: "pilot_table",
        4: "airport_table",
        5: "user_table",
    }
    #uses dictionary to set key(numerical identifier) value(table) pair
    for numericalIdentifier, databaseTable in validTables.items():
      print(f"{numericalIdentifier}) {databaseTable}")
    print("6) Return to main menu")
    #displays a footer for menu
    print(''.center(50, '-'))

    # Get the numerical choice from the user
    viewTableSelection = int(
        input("\nPlease select a table to create a listing: "))
    print("\n")
    selectedTableName = validTables.get(viewTableSelection)
    if selectedTableName is not None:
      if selectedTableName == "flight_table":
        try:
          print('Create flight entry '.center(50, '-'))

          tableDf = pd.read_sql_query("SELECT aircraft_callsign, model FROM aircraft_table", con)
          #prints tableDf is a stylised format
          print(tabulate(tableDf,headers='keys',tablefmt='fancy_grid',
                       showindex=False))
          # User input for flight data
          aircraftCallsign = input("Aircraft Callsign: ")
          tableDf = pd.read_sql_query("SELECT pilot_id, forename FROM pilot_table", con)
          #prints tableDf is a stylised format
          print(tabulate(tableDf,headers='keys',tablefmt='fancy_grid',
                       showindex=False))
          pilotId1 = input("Pilot 1 ID: ")
          pilotId2 = input("Pilot 2 ID: ")
          tableDf = pd.read_sql_query("SELECT name FROM airport_table", con)
          print(tabulate(tableDf,headers='keys',tablefmt='fancy_grid',
             showindex=False))
          departureAirport = input("Departure Airport: ")
          arrivalAirport = input("Arrival Airport: ")
          estimatedDepartureDatetime = input(
              "Estimated Departure Datetime (YYYY-MM-DD HH:MM): ")
          estimatedArrivalDatetime = input(
              "Estimated Arrival Datetime (YYYY-MM-DD HH:MM): ")
          tableDf = pd.read_sql_query("SELECT aircraft_id, model, capacity FROM aircraft_table", con)
          #prints tableDf is a stylised format
          print(tabulate(tableDf,headers='keys',tablefmt='fancy_grid',
                       showindex=False))
          passengerNumbers = input("Passenger Numbers: ")

          # converts str to datetime
          departure_datetime = datetime.strptime(estimatedDepartureDatetime,
                                                 "%Y-%m-%d %H:%M")
          # converts str to datetime
          arrival_datetime = datetime.strptime(estimatedArrivalDatetime,
                                               "%Y-%m-%d %H:%M")

          # Calculate flight duration
          flightDuration = arrival_datetime - departure_datetime

          #defines SQLite query
          addFlight = (
              "INSERT INTO flight_table (aircraft_callsign, pilot1_id, pilot2_id, departure_airport,"
              "arrival_airport, estimated_departure_datetime, "
              "estimated_arrival_datetime, flight_duration, passenger_numbers) VALUES (?,?,?,?,?,?,?,?,?)"
          )
          #executes SQLite query
          cur.execute(
              addFlight,
              (aircraftCallsign, pilotId1, pilotId2, departureAirport,
               arrivalAirport, estimatedDepartureDatetime,
               estimatedArrivalDatetime, str(flightDuration), passengerNumbers))

          #commits changes
          con.commit()

          #fetches necessary information from other tables
          cur.execute(
              "SELECT flight_id, departure_airport, arrival_airport, flight_duration FROM flight_table WHERE rowid = last_insert_rowid()"
          )
          fetchedFlightInformation = cur.fetchone()

          # Extract the required information
          flightId = fetchedFlightInformation[0]
          departureCity = fetchedFlightInformation[1]
          arrivalCity = fetchedFlightInformation[2]
          flightDuration = fetchedFlightInformation[3]

          # Fetch forename and surname from pilot_table for both pilotId1 and pilotId2
          cur.execute(
              "SELECT forename, surname FROM pilot_table WHERE pilot_id = ?",
              (pilotId1, ))
          fetchedPilotInformation1 = cur.fetchone()

          cur.execute(
              "SELECT forename, surname FROM pilot_table WHERE pilot_id = ?",
              (pilotId2, ))
          fetchedPilotInformation2 = cur.fetchone()

          # Print relevant information
          print("Flight entry successfully added")
          returnMenu()

        except ValueError:
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again
          print("Invalid input, please try again.")
          insertTableDataMenu()


      elif selectedTableName == "aircraft_table":
        try:
          print('Create aircraft entry '.center(50, '-'))

          # User input for aircraft data
          aircraftCallsign = input("Aircraft Callsign: ")
          model = input("Aircraft Model: ")
          aircraftClass = input("Aircraft Class: ")
          range_ = int(input("Aircraft Range: "))
          capacity = int(input("Aircraft Capacity: "))

          # defines SQLite query
          addAircraftQuery = (
              "INSERT INTO aircraft_table (aircraft_callsign, model, class, range, capacity) VALUES (?,?,?,?,?)"
          )
          # executes SQLite query
          cur.execute(addAircraftQuery,
                      (aircraftCallsign, model, aircraftClass, range_, capacity))

          # Commit the changes
          con.commit()

          print('Aircraft entry successfully added'.center(50, '-'))

        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again
      elif selectedTableName == "pilot_table":
        try:
          print('Create pilot entry '.center(50, '-'))

          # User input for pilot data
          forename = input("Forename: ")
          surname = input("Surname: ")
          dateOfBirth = input("Date of Birth (YYYY-MM-DD): ")
          nationality = input("Nationality: ")
          totalFlightHours = int(input("Total Flight Hours: "))
          notes = input("Notes (optional): ")

          # Insert data into pilot_table
          addPilotQuery = '''
              INSERT INTO pilot_table (
                  forename, surname, date_of_birth, nationality, total_flight_hours, notes
              ) VALUES (?, ?, ?, ?, ?, ?)
          '''

          cur.execute(addPilotQuery, (forename, surname, dateOfBirth,
                                      nationality, totalFlightHours, notes))

          # Commit the changes
          con.commit()

          print('Pilot entry successfully added'.center(50, '-'))
          returnMenu()

        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again
      elif selectedTableName == "airport_table":
        try:
          print('Create airport entry '.center(50, '-'))

          # User input for airport data
          name = input("Airport Name: ")
          city = input("City: ")
          country = input("Country: ")
          status = input("Status (hub/spoke): "
                         )  # Assuming the status can be either 'hub' or 'spoke'

          # Insert data into airport_table
          addAirportQuery = '''
              INSERT INTO airport_table (name, city, country, status) VALUES (?, ?, ?, ?)
          '''

          cur.execute(addAirportQuery, (name, city, country, status))

          # Commit the changes
          con.commit()

          print('Airport entry successfully added'.center(50, '-'))

        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again
      elif selectedTableName == "user_table":
        print('Create user entry '.center(50, '-'))
        newUserUsername = input("username: ")
        newUserPassword = input("password: ")
        newUserLevel = int(input("level: "))
        #defines SQLite query
        createNewAccount = ('''
        INSERT INTO user_table (user_username, user_password, user_level) 
        VALUES (?,?,?)
        ''')
        #executes SQLite query
        cur.execute(createNewAccount,
                    [newUserUsername, newUserPassword, newUserLevel
                     ])
        #commits changes
        con.commit()
        print('Create user entry successful!'.center(50, '-'))
        returnMenu()
      elif selectedTableName == 6:
        mainMenu()
      else:
        print("Invalid input, please try again.")
        insertTableDataMenu()
    else:
      mainMenu()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nInvalid option, please try again")
    viewTableMenu()


def modifyTableDataMenu():
  try:
    #displays a header for menu
    print(' Modify Table Entry Menu '.center(50, '-'))
    #displays menu choices
    validTables = {
        1: "flight_table",
        2: "aircraft_table",
        3: "pilot_table",
        4: "airport_table",
        5: "user_table",
    }
    #uses dictionary to set key(numerical identifier) value(table) pair
    for numericalIdentifier, databaseTable in validTables.items():
      print(f"{numericalIdentifier}) {databaseTable}")
    print("6) Return to main menu")
    #displays a footer for menu
    print(''.center(50, '-'))

    # Get the numerical choice from the user
    viewTableSelection = int(
        input(
            "\nPlease select the table containing the entry you want to modify: "
        ))
    selectedTableName = validTables.get(viewTableSelection)
    if selectedTableName is not None:
      if selectedTableName == "flight_table":
        try:
          print('Modify flight entry '.center(50, '-'))
          tableDf = pd.read_sql_query("SELECT * FROM flight_table", con)
          print(
              tabulate(tableDf,
                       headers='keys',
                       tablefmt='fancy_grid',
                       showindex=False))

          selectFlightId = input("Current Flight ID: ")
          modifiedPilotId1 = input("Modified Pilot 1 ID: ")
          modifiedPilotId2 = input("Modified Pilot 2 ID: ")
          modifiedDepartureCity = input("Modified Departure City: ")
          modifiedDepartureCountry = input("Modified Departure Country: ")
          modifiedArrivalCity = input("Modified Arrival City: ")
          modifiedArrivalCountry = input("Modified Arrival Country: ")
          modifiedEstimatedDepartureDatetime = input(
              "Modified Estimated Departure Datetime (YYYY-MM-DD HH:MM): ")
          modifiedEstimatedArrivalDatetime = input(
              "Modified Estimated Arrival Datetime (YYYY-MM-DD HH:MM): ")

          departure_datetime = datetime.strptime(
              modifiedEstimatedDepartureDatetime, "%Y-%m-%d %H:%M")
          arrival_datetime = datetime.strptime(modifiedEstimatedArrivalDatetime,
                                               "%Y-%m-%d %H:%M")
          modifiedFlightDuration = arrival_datetime - departure_datetime
          modifiedPassengerNumbers = input("Modified Passenger Numbers: ")
          #defines SQLite query
          modifyFlight = ('''UPDATE 
          flight_table SET pilot1_id = ?, pilot2_id = ?, 
          departure_city = ?, departure_country = ?, arrival_city = ?,
          arrival_country = ?, estimated_departure_datetime = ?,
          estimated_arrival_datetime = ?, flight_duration = ?,
          passenger_numbers = ?
          WHERE
          flight_id = ?;
          ''')
          #executes SQLite query
          cur.execute(
              modifyFlight,
              (modifiedPilotId1, modifiedPilotId2, modifiedDepartureCity,
               modifiedDepartureCountry, modifiedArrivalCity,
               modifiedArrivalCountry, modifiedEstimatedDepartureDatetime,
               modifiedEstimatedArrivalDatetime, str(modifiedFlightDuration),
               modifiedPassengerNumbers, selectFlightId))
          #commits changes
          con.commit()
          print('Modify flight entry successful! '.center(50, '-'))

        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again

      elif selectedTableName == "aircraft_table":
        try:
          print('Modify flight entry '.center(50, '-'))
          tableDf = pd.read_sql_query("SELECT * FROM aircraft_table", con)
          print(
              tabulate(tableDf,
                       headers='keys',
                       tablefmt='fancy_grid',
                       showindex=False))

          selectAircraftId = input("Current Aircraft ID: ")
          modifiedModel = input("Modified Model: ")
          modifiedClass = input("Modified Class: ")
          modifiedRange = input("Modified Range (miles): ")
          modifiedCapacity = input("Modified Capacity: ")

          modifyAircraft = ('''UPDATE
          aircraft_table SET model = ?, capacity = ?, 
          class = ?, range = ?
          WHERE 
          aircraft_id = ?
          ''')
          #executes SQLite query
          cur.execute(modifyAircraft,
                      (modifiedModel, modifiedCapacity, modifiedClass,
                       modifiedRange, selectAircraftId))
          #commits changes
          con.commit()
          print('Modify flight entry successful! '.center(50, '-'))
        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again

      elif selectedTableName == "pilot_table":
        try:
          print('Modify pilot entry '.center(50, '-'))
          tableDf = pd.read_sql_query("SELECT * FROM pilot_table", con)
          print(
              tabulate(tableDf,
                       headers='keys',
                       tablefmt='fancy_grid',
                       showindex=False))

          selectPilotId = input("Current Pilot ID: ")
          modifiedForename = input("Modified Forename: ")
          modifiedSurname = input("Modified Surname: ")
          modifiedDateOfBirth = input("Modified Date of Birth: ")
          modifiedNationality = input("Modified Nationality: ")
          modifiedTotalFlightHours = input("Modified Total Flight Hours: ")
          modifiedNotes = input("Modified notes: ")
          #define SQLite query
          modifyPilot = ('''UPDATE 
          pilot_table 
          SET forename = ?, surname = ?, 
          date_of_birth = ?, nationality = ?,
          total_flight_hours = ?, notes = ?
          WHERE 
          pilot_id = ?
          ''')
          #execute SQLite query
          cur.execute(modifyPilot,
                      (modifiedForename, modifiedSurname, modifiedDateOfBirth,
                       modifiedNationality, modifiedTotalFlightHours,
                       modifiedNotes, selectPilotId))
          #commit changes
          con.commit()
          print('Modify flight entry successful'.center(50, '-'))
        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again

      elif selectedTableName == "airport_table":
        try:
          #displays a header for section
          print('Modify airport entry '.center(50, '-'))
          tableDf = pd.read_sql_query("SELECT * FROM airport_table", con)
          #prints tableDf is a stylised format
          print(tabulate(tableDf,headers='keys',
                       tablefmt='fancy_grid',showindex=False))

          selectAirportId = input("Current Airport ID: ")
          modifiedName = input("Modified Airport Name: ")
          modifiedCity = input("Modified City: ")
          modifiedCountry = input("Modified Country: ")
          modifiedStatus = input("Modified Status (hub/spoke): ")
          #defines SQLite query
          modifyAirport = ('''UPDATE
          airport_table
          SET
          name = ?,
          city = ?,
          country = ?,
          status = ?
          WHERE
          airport_id = ?
          ''')
          #executes SQLite query
          cur.execute(modifyAirport,
                      (modifiedName, modifiedCity, modifiedCountry,
                       modifiedStatus, selectAirportId))
          #commits changes
          con.commit()
          #displays a footer for section
          print('Modify flight entry successful'.center(50, '-'))


        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again

      elif selectedTableName == "user_table":
        try:
          print('Modify user entry '.center(50, '-'))
          tableDf = pd.read_sql_query("SELECT * FROM user_table", con)
          print(
              tabulate(tableDf,
                       headers='keys',
                       tablefmt='fancy_grid',
                       showindex=False))

          selectUserId = input("Current user ID: ")
          modifiedUsername = input("Modified Username: ")
          modifiedPassword = input("Modified Password: ")
          modifiedLevel = input("Modified Level: ")
          #defines SQLite query
          modifyUser = ('''UPDATE 
          user_table 
          SET user_username = ?, user_password = ?, 
          user_level = ?
          WHERE 
          user_id = ?
          ''')
          #executes SQLite quer
          cur.execute(
              modifyUser,
              (modifiedUsername, modifiedPassword, modifiedLevel, selectUserId))
          #commits changes
          con.commit()
          print('Modify user entry successful'.center(50, '-'))
          #displays a footer for section

        except ValueError:
          print("Invalid input, please try again.")
          modifyTableDataMenu()
          #catches any errors (e.g., symbol or int entered)
          #invalid selection, prompts user to try again
    else:
      print("\n")
      mainMenu()
  except ValueError:
    print("Invalid input, please try again.")
    modifyTableDataMenu()
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again


def deleteTableDataMenu():
  try:
    #displays a header for menu
    print(' Delete Table Menu Entry'.center(50, '-'))
    validTables = {
      #displays menu choices
        1: "flight_table",
        2: "aircraft_table",
        3: "pilot_table",
        4: "airport_table",
        5: "user_table",
    }
    #uses dictionary to set key(numerical identifier) value(table) pair
    for numericalIdentifier, databaseTable in validTables.items():
      print(f"{numericalIdentifier}) {databaseTable}")
    print("6) Return to main menu")
    print(''.center(50, '-'))
    #displays a footer for menu

    # Get the numerical choice from the user
    viewTableSelection = int(
        input("\nPlease select a table to delete a listing: "))
    selectedTableName = validTables.get(viewTableSelection)
    if selectedTableName is not None:
      #tables are outputted as a dataframe to
      #maximise readability in tables with many columns
      tableDf = pd.read_sql_query(f"SELECT * FROM {selectedTableName}", con)
      #if the table dataframe isn't empty it will be printed
      if not tableDf.empty:
        #prints tableDf is a stylised format
        print(tabulate(tableDf,headers='keys',
                     tablefmt='fancy_grid',showindex=False))

      #if the table dataframe IS empty
      #a message will be printed, rather than an empty dataframe

      else:
        print(f"\nThe {selectedTableName} is currently empty.")
      # delete based on user input
      cur.execute(f"PRAGMA table_info({selectedTableName})")
      columns_info = cur.fetchall()
      #checks if the first column is the table's primary key
      pkColumn = next(
          (column_info[1]
           for column_info in columns_info if column_info[5] == 1),
          None,
      )
      #defines the row to be deleted
      rowValue = int(input("Enter the ID you would like to delete: "))
      deleteEntry = f"DELETE FROM {selectedTableName} WHERE {pkColumn} = ?"
      #executes SQLite query
      cur.execute(deleteEntry, (rowValue, ))
      #commits changes
      con.commit()
      print(f"\n{selectedTableName} entry deleted successfully.")
      returnMenu()
    else:
      print("\n")
      deleteTableDataMenu()
  except ValueError:
    #catches any errors (e.g., symbol or int entered)
    #invalid selection, prompts user to try again
    print("\nInvalid option selected, Please try again")
    deleteTableDataMenu()

loginRegisterMenu()
