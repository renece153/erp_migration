## Import Libraries ####
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import win32com.client
import pandas as pd
import os
from selenium.webdriver.common.action_chains import ActionChains
import sys
import log_info as sl
import mail_gun_email as mail

def initialize_driver():
    global driver
    driver = webdriver.Edge()

def get_onedrive_directory():
    home_dir = str(os.environ['SharedDrive'])
    kard_dir = 'DM'
    hr_dir = 'HR'
    sub_dir = 'Unlinking Logs'
    chk_documents = os.path.join(home_dir, kard_dir, hr_dir, sub_dir)
    if (os.path.exists(chk_documents)):
        default_path = chk_documents
    else:
        default_path = home_dir
    return default_path

def get_xlsx_file(num):
    switch = {
        1: 'HR_Unlinking_Reference_vanilla.xlsx',
        2: 'HR_Unlinking_Reference_migration.xlsx',
        3: 'HR_Unlinking_Reference_vanilla.xlsx',
        4: 'HR_Unlinking_Reference_migration.xlsx',
    }
    return switch.get(num, 'Sheet1')

def get_dynamics_url(num):
    switch = {
        1:  'URL1' ## Removed because it's the URL of the Company,
        2: 'URL2' ## Removed because it's the URL of the Company,
        3: 'URL3' ## Removed because it's the URL of the Company,
        4: 'URL4' ## Removed because it's the URL of the Company
    }
    return switch.get(num, 'https:www.google.com')

def get_environment_details(num):
    switch = {
        1: 'Vanilla Environment with OData Feed Check',
        2: 'Migration Environment with OData Feed Check',
        3: 'Vanilla Environment. Skipping OData Check',
        4: 'Migration Environment. Skipping OData Check',
    }
    return switch.get(num, 'https:www.google.com')

def convert_environment_to_number(_env : str):
    try:
        catalogue = {
            'Vanilla w/ Refresh': 1,
            'Migration w/ Refresh': 2,
            'Vanilla, No Refresh': 3,
            'Migration, No Refresh': 4,
        }
        return catalogue.get(_env)
    except Exception as e:
        sl.error(str(e))
def get_unlinking_file(num):
    return os.path.join(get_onedrive_directory(), get_xlsx_file(num))

def open_dynamics_365(num):
    try:
        driver.get(get_dynamics_url(num))
        time.sleep(5)
    except Exception as e:
        sl.error(str(e))


def search_name(_input_message):
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element("xpath", "//input[@name='QuickFilter_Input']")))
        element_var.click()
        time.sleep(2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(1)
        element_var.send_keys(_input_message)
        time.sleep(2)
        element_var.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def refresh_excel(excel_path):
    try:
        print(f"Refreshing {excel_path}")
        # Opening Excel software using the win32com
        File = win32com.client.Dispatch("Excel.Application")
        # Optional line to show the Excel software
        File.Visible = False
        # Opening your workbook
        Workbook = File.Workbooks.open(excel_path)
        # Refeshing all the shests
        Workbook.RefreshAll()

        Workbook.Application.CalculateUntilAsyncQueriesDone()

        Workbook.Application.DisplayAlerts = False
        # Saving the Workbook
        Workbook.Save()
        # Closing the Excel File
        File.Quit()
    except Exception as e:
        sl.error(str(e))

def open_excel(file_name):
    df = pd.read_excel(file_name, sheet_name='ToErase')
    return df

def open_change_timelines():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@id,'ChangesTimeline')]")))
        element_var.click()
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN).perform()
        time.sleep(1)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def open_manage_changes():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[contains(@class,'button') and contains(@id,'HcmPositionDateManager')]")))
        element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def move_to_position_worker_assignments():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@id,'WorkerAssignmentTabPage')]")))
        element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def remove_worker_assignment():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element("xpath", "//button[contains(@id,'DeleteWorkerAssignmentCommandButton')]")))
        element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def remove_positional_heirarachy():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element("xpath", "//button[contains(@id,'DeleteHierarchyCommandButton')]")))
        element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))


def confirm_removal():
    try:
        element_var = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(driver.find_element("xpath", "//button[contains(@id,'Yes')]")))
        element_var.click()
        time.sleep(3)
    except Exception as e:
        sl.error(str(e))

def move_to_position_heirarchies():
    try:
        element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@id,'HierarchyTabPage')]")))
        element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def go_back():
    try:
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        # element_var = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@id,'SystemDefinedCloseButton') and contains(@data-dyn-controlname,'SystemDefinedCloseButton')]")))
        # element_var.click()
        time.sleep(1)
    except Exception as e:
        sl.error(str(e))

def refresh_unlinking_file(_num):
    sl.alert(sl.generate_header('=', 'Refreshing Excel File Commencing'))
    file_path = get_unlinking_file(_num)
    if _num in (1,2):
        sl.alert(f"Refreshing Data from {file_path}")
        refresh_excel(file_path)
        time.sleep(2)
    else:
        sl.alert(f"Skipping Refresh of {file_path}")
    df = open_excel(file_path)
    df1_filtered = df[df['Positions'].notna()]
    df1_to_list = df1_filtered['Name']
    sl.alert(f"Loading {len(df1_to_list)} records to memory")
    sl.alert(sl.generate_header('=', 'Refreshing Excel File Complete'))
    return df1_to_list.to_list()

def step_by_step_unlinking(_env):
    _num = convert_environment_to_number(_env)
    list_of_names = refresh_unlinking_file(_num)
    sl.alert(sl.generate_header('=', 'Unlinking HR Data Start'))
    initialize_driver()
    open_dynamics_365(_num)
    _no = len(list_of_names)
    _com = 0
    for _name in list_of_names:
        sl.alert(f"Remaining Records: {_no};  Completed Records: {_com}")
        sl.alert(f"Unlinking {_name} Start")
        search_name(_name)
        open_change_timelines()
        move_to_position_worker_assignments()
        remove_worker_assignment()
        confirm_removal()
        sl.alert(f"Removing Work Assignments for {_name}")
        time.sleep(1)
        move_to_position_heirarchies()
        remove_positional_heirarachy()
        confirm_removal()
        sl.alert(f"Removing Position Heirarchy for {_name}")
        go_back()
        sl.alert(f"Unlinking {_name} Complete")
        _no -= 1
        _com += 1
    time.sleep(5)
    sl.alert(sl.generate_header('=', 'Unlinking HR Data End'))
    mail.send_message(['Rey.Torrecampo@Kardium.com','Seulah.Lee@kardium.com'])

# step_by_step_unlinking('Migration w/ Refresh')
if __name__ == "__main__":
    step_by_step_unlinking(sys.argv[1])


## step_by_step_unlinking()


## step_by_step_unlinking()
