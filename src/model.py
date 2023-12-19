# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

from datetime import datetime

# Basemodel contains the initialization for error messages
class BaseModel:
    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error


class AuthenticationModel:
    ACCESS_COLLECTION = 'users'

    def find_device_access(self, username, device_id):
        key1 = {'$or':[{'$and':[{'username':username},{'alist' : { '$elemMatch':{ 'did' :device_id , 'atype' : 'r' }}}]},{'$and':[{'username':username}, {'role': 'admin'}]}]}
        key2 = {'$or':[{'$and':[{'username':username},{'alist' : { '$elemMatch':{ 'did' :device_id , 'atype' : 'rw' }}}]},{'$and':[{'username':username}, {'role': 'admin'}]}]}
        if self.__find(key1):
            device_access = 1
        elif self.__find(key2):
            device_access = 2
        else:
            device_access = 0
        return device_access

    def find_role(self, username):
        key = {'$and':[{'username':username}, {'role': 'admin'}]}
        if self.__find(key):
            return 1
        else:
            return 0

    def __find(self, key):
        access_document = self._db.get_single_data(AuthenticationModel.ACCESS_COLLECTION, key)
        return access_document



# User document contains username (String), email (String), and role (String) fields
class UserModel(BaseModel,AuthenticationModel):
    USER_COLLECTION = 'users'

    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username, loggedin_user):
        isadmin = self.find_role(loggedin_user)
        if isadmin != 1:
            self._latest_error = 'Query failed, Admin access required!'
            return -1
        key = {'username': username}
        return self.__find(key)


    def find_role_by_username(self, username, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)
        if isadmin == 1:
            key1 = {'username': username, 'role': 'admin'}
            key2 = {'username': username, 'role': 'default'}
            if self.__find(key1):
                user_role = "admin access"
            elif self.__find(key2):
                user_role = "default access"
            else:
                self._latest_error = f'Username {username} does not exist'
                return -1
            return user_role
        else:
            self._latest_error = 'Query failed, Admin access required!'
            return -1

    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    #Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document


    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role, access, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)

        if isadmin != 1:
            self._latest_error = 'Insert failed, Admin access required!'
            return -1

        user_document = self.find_by_username(username, loggedin_user)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1
        
        user_data = {'username': username, 'email': email, 'role': role, 'alist': access}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    # This updates the user's read/write access for devices
    def update(self, username, access, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)

        if isadmin != 1:
            self._latest_error = 'Update failed, Admin access required!'
            return -1

        user_document = self.find_by_username(username, loggedin_user)

        if (user_document):
            access_data = {'alist': access}
            self._db.update_single_data(UserModel.USER_COLLECTION, {'username': username}, access_data)
            return self.find_by_username(username, loggedin_user)
        else:
            self._latest_error = f'Username {username} does not exist'
            return -1


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel(BaseModel, AuthenticationModel):
    DEVICE_COLLECTION = 'devices'

    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)
        authorized_user = self.find_device_access(loggedin_user, device_id)

        if isadmin != 1 and authorized_user == 0:
            self._latest_error = f'Read access not allowed to {device_id}!'
            return -1
        key = {'device_id': device_id}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)


    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)

        if isadmin != 1:
            self._latest_error = 'Insert failed, Admin access required!'
            return -1

        device_document = self.find_by_device_id(device_id,loggedin_user)
        if (device_document):
            self._latest_error = f'Device id {device_id} already exists'
            return -1
        
        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel(BaseModel, AuthenticationModel):
    WEATHER_DATA_COLLECTION = 'weather_data'

    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)
        authorized_user = self.find_device_access(loggedin_user, device_id)

        if isadmin != 1 and authorized_user == 0:
            self._latest_error = f'Read access not allowed to {device_id} data!'
            return -1

        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp, loggedin_user):
        self._latest_error = ''

        isadmin = self.find_role(loggedin_user)
        authorized_user = self.find_device_access(loggedin_user, device_id)

        if isadmin != 1 or authorized_user != 2:
            self._latest_error = f'User {loggedin_user} is not authorized to write to the device {device_id}!'
            return -1

        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp, loggedin_user)
        if (wdata_document):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

# Newly created Daily Reports document contains device_id, date, avg, min, max fields
class DailyReportsModel(BaseModel, AuthenticationModel):

    WEATHER_DATA_COLLECTION = 'weather_data'
    new_coll_name = 'daily_reports'

    # Sets up a new collection in database to store the reports data
    def setup_new_collection(self, new_coll_name, loggedin_user):
        self._latest_error = ''
        isadmin = self.find_role(loggedin_user)
        if isadmin != 1:
            self._latest_error = 'Setup failed, Admin access required!'
            return -1

        new_coll_status = self._db.create_coll(new_coll_name)
        return new_coll_status

    # Aggregates weather data by device and date and inserts to daily_reports collection
    def data_aggregator(self, new_coll_name, loggedin_user):
        self._latest_error = ''
        isadmin = self.find_role(loggedin_user)
        if isadmin != 1:
            self._latest_error = 'Aggregation failed, Admin access required!'
            return -1

        pipeline1 = [
                    {
                        '$group':
                            {'_id': {
                                'device_id': '$device_id',
                                'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
                            },
                                'avg_value': {'$avg': "$value"},
                                'min_value':{'$min':"$value"},
                                'max_value':{'$max':"$value"}
                            }

                    },
                    {
                        '$project':
                            {
                                '_id': 0,
                                'device_id': '$_id.device_id',
                                'avg_value': '$avg_value',
                                'min_value': '$min_value',
                                'max_value': '$max_value',
                                'date': '$_id.date'
                            }
                    }
                 ]

        agg_result = self._db.aggregate_data(WeatherDataModel.WEATHER_DATA_COLLECTION, pipeline1)
        new_coll_update = self._db.insert_many_data(new_coll_name, agg_result)
        return new_coll_update

    # Generates device report for single day
    def get_device_reports_for_date(self, new_coll_name, device_id, r_date, loggedin_user):
        self._latest_error = ''
        isadmin = self.find_role(loggedin_user)
        if isadmin != 1:
            self._latest_error = 'Daily Report read failed, Admin access required!'
            return -1

        key = {'$and':[{'date': r_date}, {'device_id': device_id}]}
        repdoc = self._db.get_single_data(new_coll_name, key)
        return repdoc


    # Generates device report for a date range
    def get_device_reports_for_daterange(self, new_coll_name, device_id, startdate, enddate, loggedin_user):
        self._latest_error = ''
        isadmin = self.find_role(loggedin_user)
        if isadmin != 1:
            self._latest_error = 'Daily Report read failed, Admin access required!'
            return -1

        key = {'$and':[{'device_id': device_id, 'date': {'$gte': startdate, '$lte': enddate}}]}
        repdoc = self._db.find_many_data(new_coll_name, key)
        return repdoc





