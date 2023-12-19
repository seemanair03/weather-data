from model import UserModel, DeviceModel, WeatherDataModel, DailyReportsModel
from datetime import datetime


# --------ANSWER SECTION--------

user_coll = UserModel()
device_coll = DeviceModel()
wdata_coll = WeatherDataModel()

reports_coll = DailyReportsModel()


print("""Hello Reviewer!
This project has been enhanced to address the scenarios based on expected sample output; 
it is to be noted that due to time limitations all the design principles have not
been considered, as well as there is limited error handling. 
Hence, it is requested to kindly provide valid inputs for 
expected scenario handling (wherever user input is required) and select the 
options in sequence as much possible to avoid exceptions due to any invalid state of data.
Thank you.
""")

# Setup access for existing users after setup.py is run. This is added to main as all the answer svcenarios are added to main
user1_document = user_coll.update('admin', [{'did': 'DT001', 'atype': 'rw'}, {'did': 'DT002', 'atype': 'rw'},
                                            {'did': 'DT003', 'atype': 'rw'}, {'did': 'DT004', 'atype': 'rw'},
                                            {'did': 'DT005', 'atype': 'rw'}, {'did': 'DH001', 'atype': 'rw'},
                                            {'did': 'DH002', 'atype': 'rw'}, {'did': 'DH003', 'atype': 'rw'},
                                            {'did': 'DH004', 'atype': 'rw'}, {'did': 'DH005', 'atype': 'rw'}],
                                  'admin')
if user1_document == -1:
    print(user_coll.latest_error)
else:
    print(user1_document)

user2_document = user_coll.update('user_1', [{'did': 'DT001', 'atype': 'r'}, {'did': 'DT003', 'atype': 'rw'},
                                             {'did': 'DT005', 'atype': 'r'}, {'did': 'DH001', 'atype': 'r'},
                                             {'did': 'DH002', 'atype': 'r'}, {'did': 'DH003', 'atype': 'r'},
                                             {'did': 'DH004', 'atype': 'r'}, {'did': 'DH005', 'atype': 'r'}],
                                  'admin')
if user2_document == -1:
    print(user_coll.latest_error)
else:
    print(user2_document)

user3_document = user_coll.update('user_2', [{'did': 'DT001', 'atype': 'r'}, {'did': 'DT002', 'atype': 'r'},
                                             {'did': 'DT003', 'atype': 'r'}, {'did': 'DT004', 'atype': 'r'},
                                             {'did': 'DT005', 'atype': 'r'}, {'did': 'DH001', 'atype': 'r'},
                                             {'did': 'DH002', 'atype': 'r'}, {'did': 'DH003', 'atype': 'r'},
                                             {'did': 'DH004', 'atype': 'r'}, {'did': 'DH005', 'atype': 'r'}],
                                  'admin')
if user3_document == -1:
    print(user_coll.latest_error)
else:
    print(user3_document)
print("device access updated for existing users!")


option = "-1"
while option!="0":

    option = (input("""
    The 'expected_sample_output.txt' file had below test scanarios to be covered in the answer code:-
    
    1-Does 'admin' have admin access? OR Does 'user_1' have admin access?
    2-Is username based query possible for 'admin'? OR Is username based query possible for 'user_1'?
    3-Can 'admin' add a new user? OR Can 'user_1' add a new user?
    4-Can 'admin' access device DT004? OR Can 'user_1' access device DT004? OR Can 'user_1' access device DT001?
    5-Can 'admin' create device DT201? OR Can 'user_1' create device DT202?
    6-Can 'admin' read DT001 device data? OR Can 'user_1' read DT001 device data? OR Can 'user_1' read DT002 device data?
    7-Create new collection 'daily_reports' in weather_db and insert aggregate data from weather collection
    8-(prerequisite - execute scenario 7 at-least once before 8) Get daily report for one day 
    9-(prerequisite - execute scenario 7 at-least once before 9) Get daily report for multiple days
    
    0-EXIT
    
    Pick a scenario to execute: """))

    if option=="0":
        print("You decided to exit. Thank you!")
        exit()

    a_username = input("Please provide your login username: ")
    # Shows an unsuccessful read on user collection
    user_document = user_coll.find_by_username(a_username,'admin')
    if user_document == None:
        print("Login user does not exist, please try again with a valid user!")
        exit()



    # 1-Does 'admin' have admin access?
    # True
    if option == "1":
        user_n = input("Provide username (example admin): ")
        user_document = user_coll.find_role_by_username(user_n, a_username)
        if user_document == -1:
            print(user_coll.latest_error)
        else:
            print(user_document)

    # 2-Is username based query possible for 'admin'?
    # {'_id': ObjectId('61484f849afa055fc11c6fb9'), 'username': 'user_2', 'email': 'user_2@example.com', 'role': 'default', 'alist': [{'did': 'DT002', 'atype': 'r'}, {'did': 'DT003', 'atype': 'r'}]}
    elif option == "2":
        user_n = input("Provide username (example user_2): ")
        user_document = user_coll.find_by_username(user_n, a_username)
        if user_document==-1:
            print(user_coll.latest_error)
        else:
            print(user_document)

    # 3-Can 'admin' add a new user?
    # {'_id': ObjectId('6148504c696a3885597c4a02'), 'username': 'user_3', 'email': 'user_3@example.com', 'role': 'default', 'alist': [{'did': 'DT004', 'atype': 'r'}, {'did': 'DH003', 'atype': 'rw'}]}
    elif option == "3":
        user_n = input("Provide username (example user_3): ")
        user_e = input("Provide email (example user_3@example.com): ")
        user_document = user_coll.insert(user_n, user_e, 'default', [{'did': 'DT004', 'atype': 'r'}, {'did': 'DH003', 'atype': 'rw'}] ,a_username)
        if user_document == -1:
            print(user_coll.latest_error)
        else:
            print(user_document)

    # 4-Can 'admin' access device DT004?
    # {'_id': ObjectId('61484f849afa055fc11c6fbd'), 'device_id': 'DT004', 'desc': 'Temperature Sensor', 'type': 'Temperature', 'manufacturer': 'Acme'}
    elif option == "4":
        device_d = input("Provide device id (example DT004): ")
        device_document = device_coll.find_by_device_id(device_d, a_username)
        if device_document ==-1:
            print(device_coll.latest_error)
        else:
            print(device_document)

    # 5-Can 'admin' create device DT201?
    # {'_id': ObjectId('6148504c696a3885597c4a03'), 'device_id': 'DT201', 'desc': 'Temperature Sensor', 'type': 'Temperature', 'manufacturer': 'Acme'}
    elif option == "5":
        device_d = input("Provide device id (example DT201): ")
        device_document = device_coll.insert(device_d, 'Temperature Sensor', 'Temperature', 'Acme', a_username)
        if device_document == -1:
            print(device_coll.latest_error)
        else:
            print(device_document)

    # 6-Can 'admin' read DT001 device data?
    # {'_id': ObjectId('61484f859afa055fc11c6fe9'), 'device_id': 'DT001', 'value': 27, 'timestamp': datetime.datetime(2020, 12, 2, 13, 30)}
    elif option == "6":
        device_d = input("Provide device id (example DT001): ")
        wdata_document = wdata_coll.find_by_device_id_and_timestamp(device_d, datetime(2020, 12, 2, 13, 30), a_username)
        if wdata_document==-1:
            print(wdata_coll.latest_error)
        else:
            print(wdata_document)

    # Does 'user_1' have admin access?
    # False
    # Re-run scenario number 1 with 'user_1'

    # Is username based query possible for 'user_1'?
    # Query failed, Admin access required!
    # Re-run scenario number 2 with 'user_1'

    # Can 'user_1' add a new user?
    # Insert failed, Admin access required!
    # Re-run scenario number 3 with 'user_1'

    # Can 'user_1' access device DT004?
    # Read access not allowed to DT004
    # Re-run scenario number 4 with 'user_1'

    # Can 'user_1' access device DT001?
    # {'_id': ObjectId('61484f849afa055fc11c6fba'), 'device_id': 'DT001', 'desc': 'Temperature Sensor', 'type': 'Temperature', 'manufacturer': 'Acme'}
    # Re-run scenario number 4 with 'user_1' and 'DT001'


    # Can 'user_1' create device DT202?
    # Insert failed, Admin access required!
    # Re-run scenario number 5 with 'user_1'


    # Can 'user_1' read DT001 device data?
    # {'_id': ObjectId('61484f859afa055fc11c6fe9'), 'device_id': 'DT001', 'value': 27, 'timestamp': datetime.datetime(2020, 12, 2, 13, 30)}
    # Re-run scenario number 6 with 'user_1' and DT001


    # Can 'user_1' read DT002 device data?
    # Read access not allowed to DT002 data
    # Re-run scenario number 6 with 'user_1' and DT002



    # 7---------Generate daily reports-------
    # Create new collection 'daily_reports' in weather_db and insert aggregate data from weather collection.
    elif option == "7":
        # Creates new collection named 'daily_reports' in 'weather_db' database.
        new_collection_name = "daily_reports"
        coll_create_success = False
        reports_document = reports_coll.setup_new_collection(new_collection_name, a_username)
        if reports_document == -1:
            print(reports_coll.latest_error)
        else:
            if reports_document != None:
                coll_create_success = True
                print("New collection '"+ new_collection_name +"' created successfully!")
            else:
                coll_create_success = False
                print("New collection '"+ new_collection_name +"' could not be created!")

        # Aggregates weather data from weather_data collection and inserts into the new collection
        if coll_create_success == True:
            agg_document = reports_coll.data_aggregator(new_collection_name, a_username)
            if agg_document == -1:
                print(reports_coll.latest_error)
            else:
                print("Daily report one time bulk insert done!")
        else:
            print("Daily report one time bulk insert failed!")

    # 8-Get daily report for one day
    # {'device_id': 'DT004', 'avg_value': 23.58, 'min_value': 18, 'max_value': 27, 'date': '2020-12-02'}
    elif option == "8":
        r_device = input("Provide device id (example DT001): ")
        r_date = input("Provide date in yyyy-mm-dd format (example 2020-12-01): ")
        d_report = reports_coll.get_device_reports_for_date('daily_reports', r_device, r_date, a_username)
        if d_report == -1:
            print(reports_coll.latest_error)
        else:
            print("Report for a single day:-")
            print(d_report)



        # 9-Get daily report for multiple days
        # [{'device_id': 'DT004', 'avg_value': 23.46, 'min_value': 20, 'max_value': 28, 'date': '2020-12-03'}, {'device_id': 'DT004', 'avg_value': 23.58, 'min_value': 18, 'max_value': 27, 'date': '2020-12-02'}, {'device_id': 'DT004', 'avg_value': 23.21, 'min_value': 18, 'max_value': 26, 'date': '2020-12-04'}]
    elif option == "9":
        r_device = input("Provide device id (example DT001): ")
        s_date = input("Provide start date in yyyy-mm-dd format (example 2020-12-01): ")
        e_date = input("Provide end date in yyyy-mm-dd format (example 2020-12-05): ")
        d_report = reports_coll.get_device_reports_for_daterange('daily_reports', r_device, s_date,e_date, a_username)
        if d_report == -1:
            print(reports_coll.latest_error)
        else:
            print("Report for a multiple days:-")
            for r_document in (d_report):
                print(r_document)



    else:
        print("Incorrect selection of test scenario option, please try again!")