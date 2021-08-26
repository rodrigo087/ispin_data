# Global variables
username = None
password = None



# Functions
def __authorize():
    """
    User authentication
    """

    import requests
    from retry import retry
    global username
    global password
    requests.packages.urllib3.disable_warnings()
  
    # Get access token...
    parameters = {'grant_type': 'password', 'username': username, 'password':password}
    
    @retry(tries=2, delay=30) # Retry twice.
    def post_token():      
        __baseUrl = "https://api.romowind.net/api"
        response = requests.post(__baseUrl + "/token", data=parameters, verify=False)
        return response

    if (username==None) & (password==None):
        raise Exception("Please provide your username and password as follows:\n import ispin_data.api as ispin\n ispin.username = 'your_username'\n ispin.password = 'your_password'")
        
    response = post_token()
    authResponse = response.json()
    
    # Check if the authentication was successful
    if 'error' in authResponse.keys():
        if authResponse['error'] == 'invalid_grant':
            raise Exception('Invalid username and password')
        if authResponse['error'] == 'unauthorized_client':
            raise Exception('If you are using this service for the first time, you need to log in to "https://api.romowind.net/" with your username, password and the code that was sent to your email.\nThen you can come back and run this function again')
    else:
        accessToken = authResponse['access_token']
        authHeader_base = {'Authorization': 'Bearer '+accessToken}
    
        return authHeader_base



def request_overview():
    """
    Loads an overview of the iSpin installations
    
    Returns
    ------------
    df : DataFrame
        DataFrame with information of the iSpin installation, where the index corresponds to the turbine ID
    """  
    
    import requests
    import pandas as pd

    # Obtaining authentication token
    authHeader = __authorize()
    
    # Requesting the turbines data
    __baseUrl = "https://api.romowind.net/api"
    URL = __baseUrl + '/turbines'
    response = requests.get(URL, headers=authHeader, verify=False)
    Dataresponse = response.json()
    
    # Formatting the output data frame
    df = pd.DataFrame(Dataresponse)
    df.insert(0, 'turbineID', df.id)
    df = df.set_index('id')
    
    return df



def request_data(turb, start_date=None, end_date=None):
    """
    Loads iSpin data for a turbine ID
    
    Parameters
    --------------
    turb : int
        Turbine ID for the data to be loaded (see "request_overview()")
    start_date : str
        staring date of the data to be loaded in the format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
    end_date : str
        ending date of the data te be loaded in the format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'

    Returns
    ------------
    df : DataFrame
        DataFrame with the iSpin measurements of the requested wind turbine for the selected period of time 
    """  
    
    import pandas as pd
    import requests
    import datetime
    
    # start and end date format
    if type(turb) != int:
        raise Exception('Please set the turbine ID as an integer')
    if (start_date != None) | (end_date != None):
        if (type(start_date) != str) or (type(end_date) != str):
            raise Exception('Please state the start and the end dates as strings in the format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"')
    
    # Get all data if the start and end date are not specified
    if start_date == None:
        start_date = '2010-01-01'
    if end_date == None:
        end_date = str(datetime.datetime.now())[0:10]
    
    # Obtaining authentication token
    authHeader = __authorize() 
    
    # Requesting the data
    __baseUrl = "https://api.romowind.net/api"
    URL = __baseUrl + '/turbines/%d/data?fromTime=%s&toTime=%s' % (turb, start_date, end_date)
    response = requests.get(URL, headers=authHeader, verify=False)
    Dataresponse = response.json()
    
    # Error messages if the request fails
    if type(Dataresponse) == list:
        if Dataresponse == []:
            raise Exception('No data in the selected period')
    else:
        if 'not found' in Dataresponse['message']:
            raise Exception('The requested turbine was not found. Check that you have the right permissions to load data for this turbine')
        if 'No data service' in Dataresponse['message']:
            raise Exception('No data service for this turbine is enabled. Please contact Nabla Wind Hub if you would like to get data access for this turbine')
        if 'request is invalid' in Dataresponse['message']:
            raise Exception('Please doublecheck the date format that was given to request the data')

    # Formatting the output DataFrame
    df = pd.DataFrame(Dataresponse)
    df.sampleTime = pd.to_datetime(df.sampleTime)
    df = df.set_index('sampleTime')
    df.index = df.index.tz_localize(None)
       
    # Sorting the columns
    if 'metDataValid' in df.columns:
        df = df.drop(['metDataValid'], axis=1)      
    df = df.reindex(sorted(df.columns), axis=1)
    
    return df



