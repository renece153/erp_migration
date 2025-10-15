from zeep import Client
from zeep.transports import Transport
from requests import Session
import logging
import logging.config
from zeep.wsse.username import UsernameToken
import json
from zeep.helpers import serialize_object
import pandas as pd
import dm_get_azure_db_credentials as az_log


def get_nested_value(data, path):
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list):
            if data and isinstance(data[0], dict):
                data = data[0].get(key)
            else:
                return None
        else:
            return None
    return data


logging.config.dictConfig({
    'version': 1,
    'formatters': {
     'verbose': {'format': '%(name)s: %(message)s'}},'handlers': {
    'console': {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'verbose',},},
    'loggers': {'zeep.transports': {'level': 'DEBUG','propagate': True,'handlers': ['console'],},}
})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


COMPANY_NAME = "Redacted"
USERNAME = "Redacted"
PASSWORD = "Redacted"


# Step 1: Initial WSDL
initial_wsdl = "Redacted"


# Setup transport with timeout
session = Session()
transport = Transport(session=session, timeout=300)


# Step 2: Create initial client
client = Client(wsdl=initial_wsdl, transport=transport,wsse=UsernameToken(USERNAME, PASSWORD))

try:
    response = client.service.GetClientSiteUri(COMPANY_NAME)
    if response['Error']['Code'] != 0:
        logger.error(f"Error: {response['Error']['Code']}")
        logger.error(f"Message: {response['Error']['Message']}")
        exit()

    client_uri = response['Uri']
    logger.info(f"Client Site URI: {client_uri}")

    if client_uri.lower() != client.wsdl.location.lower():
        logger.info(f"Reconnecting to DayforceService at {client_uri}")
        client = Client(wsdl=client_uri + '?wsdl', transport=transport)

    for service in client.wsdl.services.values():
        for port in service.ports.values():
            print(f"\nPort: {port.name}")
            operations = port.binding._operations
            for name, operation in operations.items():
                print(f"Operation: {name}")
                print(f"Input: {operation.input.signature()}")

    auth_params = {
    'companyName': COMPANY_NAME,
    'userName': USERNAME,
    'password': PASSWORD
    }

    auth_response = client.service.Authenticate(**auth_params)

    if auth_response['Error']['Code'] != 0:
        logger.error(f"Authentication Error: {auth_response['Error']['Code']}")
        logger.error(f"Message: {auth_response['Error']['Message']}")
        exit()


# Step 6: Extract session info
    session_ticket = auth_response['SessionTicket']
    max_query_results = auth_response['MaximumQueryResults']


    logger.info(f"Session Ticket: {session_ticket}")
    logger.info(f"Max Query Results: {max_query_results}")


except Exception as e:
    logger.exception("An error occurred during the Dayforce client operation.")



try:
    # Create the request object
    GetEmployeesRequest = client.get_type("{http://Dayforce/Services/Data}GetEmployeesRequest")
    request = GetEmployeesRequest(IncludeSubordinateObjects=True)


    response = client.service.Query(session_ticket, request)


    if response.Error.Code == 0:
        response_dict = serialize_object(response)

        employee_data = response_dict['Result']['DFObject']

        ## print(employee_data[0]['EmployeeOrgUnits']['EmployeeOrgUnitInfo'][0]['Department'].keys())
        # print(employee_data)
        fields_to_extract = []

        _list = az_log.exract_list_of_fields()
        for i in range(len(_list)):
            fields_to_extract.append(_list[i][0])

        employee_list = []

        for emp in employee_data:
            if isinstance(emp, dict):
                emp_info = {field.replace('.', '_').lower(): get_nested_value(emp, field) for field in fields_to_extract}
                employee_list.append(emp_info)

        df = pd.DataFrame(employee_list)
        df.to_sql(con=az_log.output_engine(), name='day_force_data', if_exists='replace')
    else:
        print(f"Error: {response.Error.Code}")
        print(f"Message: {response.Error.Message}")
except Exception as e:

    logger.exception("An error occurred during the Dayforce client operation.")
