import requests
import webbrowser
from flask import Flask, request, redirect
from msal import ConfidentialClientApplication
import pandas as pd
import dm_get_azure_db_credentials as az_log


# === Configuration ===
client_id = "be630b6c-fa9a-408a-a4ba-36893009d956"
tenant_id = "91aaadf7-17fe-4e27-8046-10d35b53e9eb"
client_secret = "~D08Q~WrDwRcqqZB0ALzQ52BnDBaV9B~qu9rua9L"
redirect_uri = "http://localhost:5000/getAToken" # Must match what's in Azure AD
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://kardium-migrationb60486bc1b9785abdevaos.axcloud.dynamics.com/.default"]


app = Flask(__name__)

app_msal = ConfidentialClientApplication(client_id,authority=authority,client_credential=client_secret)

def entity_name(num):
    switch = {
        0: 'EmployeesV2',
        1: 'EmploymentEmployees',
        2: 'PayrollEmployeesV2',
        3: 'BenefitsPlanEmployeesV2',
        4: 'Jobs',
        5: 'PositionsV2',
        6: 'PositionHierarchies',
        7: 'DepartmentsV2'
    }
    return switch.get(num, '')

def table_names_name(num):
    switch = {
        0: 'employees_v2',
        1: 'employment_employees',
        2: 'payroll_employees_v2',
        3: 'benefits_plan_employees_v2',
        4: 'jobs',
        5: 'positions_v2',
        6: 'position_hierarchies',
        7: 'departments_v2'
    }
    return switch.get(num, '')


@app.route('/')
def index():
    auth_url = app_msal.get_authorization_request_url(scopes=scope,redirect_uri=redirect_uri)
    return redirect(auth_url)

@app.route('/getAToken')
def get_a_token():
    code = request.args.get('code')
    result = app_msal.acquire_token_by_authorization_code(code=code, scopes=scope, redirect_uri=redirect_uri)

    if "access_token" in result:
        access_token = result['access_token']
        for i in range(0,8):
            _ext =entity_name(i)
            odata_url = f"https://kardium-migrationb60486bc1b9785abdevaos.axcloud.dynamics.com/data/{_ext}"
            headers = {"Authorization": f"Bearer {access_token}","Accept": "application/json"}

            response = requests.get(odata_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['value'])
                df.to_sql(con=az_log.output_engine(), name=table_names_name(i), if_exists='replace')

        return f"Response status: {response.status_code}"
    else:
        return f"Failed to acquire token: {result.get('error_description')}"



if __name__ == '__main__':
    app.run(port=5000)

