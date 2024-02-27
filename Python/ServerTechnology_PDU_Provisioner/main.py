from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.options import FirefoxProfile
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from shutil import get_terminal_size
from threading import Thread
from itertools import cycle
import getpass
from getpass import getpass
from time import sleep
import time
from pysnmp.hlapi import *
from pysnmp import *
import pysnmp
import sys
import os

'''Colour for text Class'''
class TEXT_COLOURS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''Loading Bar Class'''
class LOADING_BAR:
    def __init__(self, desc=f"{TEXT_COLOURS.OKBLUE}Loading...{TEXT_COLOURS.ENDC}", end=f"{TEXT_COLOURS.OKGREEN}Done!\nFinished running task(s)!\n{TEXT_COLOURS.ENDC}", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['|', '/', '-', '\\']

        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

'''Send new OID value to PDU with SNMPv1 '''
def set_oid_with_value(oid_value , value , target_ip_address):
    errorIndication, errorStatus, errorIndex, varBinds = next(
    setCmd(SnmpEngine(),
            CommunityData("private"),
            UdpTransportTarget((target_ip_address,161)),ContextData(),
            ObjectType(ObjectIdentity(oid_value),Integer(value))
        )
    )

'''Turns ON one or multiple power outlets'''
def power_outlet_ON(oid_value , target_ip_address):
    clear_screen()
    prompt = ''
    prompt = str(input(prompt+'1. Power ON single port\n2. Power ON all ports\n3. <<< Back\n> ')).lower().strip()
    if prompt == '1':  # Power OFF a single port
        user_confirmation = ''
        print(f'{TEXT_COLOURS.FAIL}This will power on a power outlet, are you sure you want to continue?\n{TEXT_COLOURS.ENDC}')
        user_confirmation = str(input(user_confirmation+'Y/N\n> ')).lower().strip()
        if user_confirmation == 'y':
            oid_value = '.1.3.6.1.4.1.19536.10.1.5.2.1.10.1.'
            power_on_this_outlet = ''
            power_on_this_outlet = str(input(power_on_this_outlet+'Which outlet should turn ON ?\n')) 
            print("Powering on specified outlet, please wait.")
            oid_value +=power_on_this_outlet
            print('\nTargeting OID value : ',oid_value)
            with LOADING_BAR("Please wait, running task(s)... "):
                time.sleep(0.25)
                oid_value = oid_value + power_on_this_outlet
                set_oid_with_value(oid_value,2,target_ip_address) 
                print('\n This port is now powered ON : Port '+power_on_this_outlet, end = '')
                print('\n')
            time.sleep(3)
            clear_screen()
        elif user_confirmation =='n':
            clear_screen()
    elif prompt == '2': # Power ON all ports  
        user_confirmation = ''
        print(f'{TEXT_COLOURS.FAIL}This will power on ALL power outlets, are you sure you want to continue?\n{TEXT_COLOURS.ENDC}')
        user_confirmation = str(input(user_confirmation+'Y/N\n> ')).lower().strip()
        if user_confirmation == 'y':
                print("Powering ON all outlets, please wait as this takes a minute or two.")
                f = open("all_ports.txt", "r") # Read file to get outlets
                with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
                    time.sleep(0.25)
                    for x in f:
                        oid_value = '.1.3.6.1.4.1.19536.10.1.5.2.1.10.1.'
                        oid_value = oid_value + x
                        print('\nTargeting OID value : ',oid_value)
                        set_oid_with_value(oid_value,2,target_ip_address)
                        print('Powered on outlet '+x, end = '')
                    print('\nAll outlets have been turned ON.\n')
                    time.sleep(3)
                    f.close()
                clear_screen()
        elif user_confirmation =='n':
            print('\nCancelling operation!')
            time.sleep(1.5)
            clear_screen()
    elif prompt == '3': # Goes back
        clear_screen()

'''Turns OFF one or multiple power outlets'''
def power_outlet_OFF(oid_value,target_ip_address):
    clear_screen()
    prompt = ''
    prompt = str(input(prompt+'1. Power OFF single port\n2. Power OFF all ports\n3. <<< Back\n> ')).lower().strip()
    if prompt == '1':  # Power OFF a single port
        user_confirmation = ''
        print(f'{TEXT_COLOURS.FAIL}This operation will power OFF a power outlet. The consequences of this action may be severe. \nContinue?\n{TEXT_COLOURS.ENDC}')
        user_confirmation = str(input(user_confirmation+'Y/N\n> ')).lower().strip()
        if user_confirmation == 'y':
            power_off_this_outlet = ''
            power_off_this_outlet = str(input(power_off_this_outlet+'Which outlet should turn OFF ?\n')) 
            print("Powering off the specified power outlet, please wait.")
            oid_value = '.1.3.6.1.4.1.19536.10.1.5.2.1.10.1.'
            oid_value = oid_value + power_off_this_outlet
            print('\nTargeting OID value : ',oid_value)
            with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
                    time.sleep(0.25)
                    set_oid_with_value(oid_value,1,target_ip_address) 
                    print('\n This port is now powered off : Port '+power_off_this_outlet, end = '')
                    print('\n')
            time.sleep(3)
        elif user_confirmation =='n':
            clear_screen()
    elif prompt == '2': # Power OFF all ports  
        user_confirmation = ''
        print(f'{TEXT_COLOURS.FAIL}This operation will power OFF a power outlet. The consequences of this action may be severe. \nContinue?\n{TEXT_COLOURS.ENDC}')
        user_confirmation = str(input(user_confirmation+'Y/N\n> ')).lower().strip()
        if user_confirmation == 'y':
            print("Powering OFF all power outlets, please wait as this takes a minute or two.")
            f = open("all_ports.txt", "r") # Read file to get outlets
            with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
                time.sleep(0.25)
                for x in f:
                    oid_value = '.1.3.6.1.4.1.19536.10.1.5.2.1.10.1.'
                    oid_value = oid_value + x
                    print('Targeting OID value : ',oid_value)
                    set_oid_with_value(oid_value,1,target_ip_address)
                    print('Powered off power outlet '+x, end = '')
            print('\nAll outlets have been turned off.\n')
            time.sleep(3)
            f.close()
        elif user_confirmation =='n':
            clear_screen()
    elif prompt == '3': # Power off based on rack standard
        clear_screen()

'''Power ON/OFF menu selection'''
def power_options(target_ip_address):
    runtime = True
    while runtime == True:
        clear_screen()
        prompt = ''
        oid_value = '.1.3.6.1.4.1.19536.10.1.5.2.1.10.1.'
        prompt = str(input(prompt+'1. Power OFF\n2. Power ON\n3. <<< Go back\n> ')).lower().strip()
        if prompt == '1':    # Power OFF
            power_outlet_OFF(oid_value,target_ip_address)
        if prompt == '2':    # Power ON
            power_outlet_ON(oid_value,target_ip_address)
        if prompt == '3':    # Go back
            clear_screen()
            runtime = False

'''Configures the PDU hardware, reboots the PDU, renames power outlets & SNMP GET for current PDU configuration'''
def hardware_configuration_options(target_ip_address,configuration_ip_address,rack_name,rack_location,contact_name,default_gateway,subnet_mask,new_pdu):
    prompt = ''
    prompt = str(input(prompt+'1. Program rPDU\n2. Reboot Network Interface and PDU \n3. Check Config\n4. <<< Go back\n> ')).lower().strip()
    if prompt == '1':
        run_pdu_configuration(target_ip_address,configuration_ip_address,rack_name,rack_location,contact_name,default_gateway,subnet_mask,new_pdu) 
    elif prompt == '2':
        user_confirmation = ''
        print(f'{TEXT_COLOURS.FAIL}This will reset the network interface and reboot the PDU\nMake sure this is what you want to do.\nContinue?\n{TEXT_COLOURS.ENDC}')
        print(f'This will {TEXT_COLOURS.FAIL}NOT{TEXT_COLOURS.ENDC} cut the power to the PDU, you will {TEXT_COLOURS.FAIL}NOT{TEXT_COLOURS.ENDC} lose energy to the outlets.')
        user_confirmation = str(input(user_confirmation+'Y/N\n> ')).lower().strip()
        if user_confirmation == 'y':
            print('Resetting Network Interface, connection may drop. PDU reboot will commence shortly')
            with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
                time.sleep(0.25)
                value = '1'
                oid_value = '.1.3.6.1.4.1.19536.10.1.1.3.1.10.1'
                set_oid_with_value(oid_value,value,target_ip_address)
                time.sleep(10)
        elif user_confirmation =='n':
                print('Cancelling operation!\n\n')
                time.sleep(1.5)
                clear_screen()
    elif prompt == '3':
        print("\n-------------------------------\nPDU configuration is :\n-------------------------------\n\n")
        show_pdu_configuration(target_ip_address)
    elif prompt == '4':
        clear_screen()

'''SNMP GET request for current PDU configuration'''
def show_pdu_configuration(target_ip_address):
    clear_screen()
    print("PDU Configuration : ")
    with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
        time.sleep(0.25)
        # Performs the GET command
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((target_ip_address, 161)), ContextData(),
                ObjectType(ObjectIdentity('.1.3.6.1.4.1.19536.10.1.1.2.1.2.1')), # PDU Name
                ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.6.0')) # PDU Location
            )
        )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
    print('')
    user_confirmation = ''
    user_confirmation = str(input(user_confirmation+'Press ENTER to go back.\n')).lower().strip()
    clear_screen()

'''Configure the PDU'''
def run_pdu_configuration(target_ip_address,configuration_ip_address,rack_name,rack_location,contact_name,default_gateway,subnet_mask,new_pdu):
    i = 1
    user_confirmation = ''
    clear_screen()
    print('Applying this configuration to the PDU:\n')
    print(f'{rack_name}\n{rack_location}\n{configuration_ip_address}\n{subnet_mask}\n{default_gateway}')
    user_confirmation = str(input(user_confirmation+'\nContinue?\nY/N\n> ')).lower().strip()
    if user_confirmation == 'y':
        web_browser_username = ''
        web_browser_password = ''
        web_browser_username = str(input(web_browser_username+'Enter the PDU username\n'))
        print('Enter the PDU password')
        web_browser_password = getpass()
        with LOADING_BAR(f"{TEXT_COLOURS.OKBLUE}PLEASE WAIT, performing task(s)... {TEXT_COLOURS.ENDC}"):
            time.sleep(0.25)
            time.sleep(4)

            # SET the PDU Name field OID = .1.3.6.1.4.1.19536.10.1.1.2.1.2.1
            if i == 1:
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    setCmd(SnmpEngine(),
                            CommunityData("private"),
                            UdpTransportTarget((target_ip_address,161)),ContextData(),
                            ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0'),
                                    OctetString(rack_name)) ))
            # SET the PDU Rack Name field OID = .1.3.6.1.2.1.1.6.0
            if i == 1:
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    setCmd(SnmpEngine(),
                            CommunityData("private"),
                            UdpTransportTarget((target_ip_address,161)),ContextData(),
                            ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.6.0'),
                                    OctetString(rack_location)) ))

            options = FirefoxOptions()
            options.set_preference("dom.webnotifications.serviceworker.enabled", False)
            options.set_preference("dom.webnotifications.enabled", False)

            # A custom profile that uses the fastest settings to load the web session
            fast_firefox_profile = {
                'dom.ipc.plugins.enabled.libflashplayer.so':False,
                'network.http.pipelining':True,
                'network.http.proxy.pipelining': True,
                'network.http.pipelining.maxrequests': 8,
                'content.notify.interval': 500000,
                'content.notify.ontimer': True,
                'content.switch.threshold': 250000,
                'browser.cache.memory.capacity': 65536,
                'browser.startup.homepage': 'about:blank',
                'reader.parse-on-load.enabled': False,
                'browser.pocket.enabled': False,
                'loop.enabled': False,
                'browser.chrome.toolbar_style': 1,
                'browser.display.show_image_placeholders': False,
                'browser.display.use_document_colors': False,
                'browser.display.use_document_fonts': 0,
                'browser.display.use_system_colors': True,
                'browser.formfill.enable': False,
                'browser.helperApps.deleteTempFileOnExit': True,
                'browser.shell.checkDefaultBrowser': False,
                'browser.startup.homepage': 'about:blank',
                'browser.startup.page': 0,
                'browser.tabs.forceHide': True,
                'browser.urlbar.autoFill': False,
                'browser.urlbar.autocomplete.enabled': False,
                'browser.urlbar.showPopup': False,
                'browser.urlbar.showSearch': False,
                'extensions.checkCompatibility': False,
                'extensions.checkUpdateSecurity': False,
                'extensions.update.autoUpdateEnabled': False,
                'extensions.update.enabled': False,
                'general.startup.browser': False,
                'plugin.default_plugin_disabled': False,
                'permissions.default.image': 2,
                }
            profile = FirefoxProfile()
            for name, value in fast_firefox_profile.items() :
                profile.set_preference(name,value)
            fast_firefox_profile = webdriver.FirefoxProfile()

            web = webdriver.Firefox(executable_path='geckodriver',options=options,firefox_profile=profile)
            pdu_url = ''
            pdu_url = 'https://'
            pdu_url = pdu_url +target_ip_address
            pdu_url = pdu_url + '/'
            web.get(pdu_url)
            time.sleep(2.5)

            username_field = web.find_element(By.XPATH,'//*[@id="username"]').send_keys(web_browser_username)
            password_field = web.find_element(By.XPATH,'//*[@id="password"]').send_keys(web_browser_password)
            submit_credentials_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/div/div[3]/div/div/form/footer/button').click()
            time.sleep(5)
            header_bar_dropdown = web.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/header/div[2]/div[1]/div[5]/div/button/span').click()
            configuration_button = web.find_element(By.XPATH,'/html/body/div[1]/div/div/nav/a[1]/span').click()
            time.sleep(3)
            configuration_dropdown_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/header/a/strong/span').click()
            time.sleep(2)
            edit_configuration_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/form/div[2]/fieldset/div[1]/span/label[2]/span[1]').click()
            time.sleep(2)
            ip_address_field_clear = web.find_element(By.XPATH,'//*[@id="ipaddress"]').clear_screen()
            ip_address_field_edit = web.find_element(By.XPATH,'//*[@id="ipaddress"]').send_keys(configuration_ip_address)
            time.sleep(2)
            netmask_field_clear = web.find_element(By.XPATH,'//*[@id="netmask"]').clear_screen()
            netmask_field_edit = web.find_element(By.XPATH,'//*[@id="netmask"]').send_keys(subnet_mask)
            time.sleep(2)
            default_gateway_field_clear = web.find_element(By.XPATH,'//*[@id="gateway"]').clear_screen()
            default_gateway_field_edit = web.find_element(By.XPATH,'//*[@id="gateway"]').send_keys(default_gateway)
            time.sleep(2)
            save_changes_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/form/footer/nav/button/span/span').click()
            confirm_changes_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/div/form/div[2]/fieldset/div/span/label/span[1]/span').click()
            logout_button = web.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/div/form/footer/div/div[1]/button/span/span').click()
            time.sleep(5)
            web.quit()
            time.sleep(40)

            print('\nConfiguration has been applied\n')
            time.sleep(5)
            clear_screen()

'''Load in the rack configuration .csv file'''
def pdu_configuration_finder():
    rack_name = ''
    rack_location = ''
    contact_name = ''
    configuration_ip_address = ''
    default_gateway = ''
    subnet_mask = ''
    logical_rack_number = ''
    target_ip_address = ''

    new_pdu = True
    target_ip_address = '192.168.0.1'
    connected_rack = 'RMA / New PDU'
    logical_rack_number = str(input(logical_rack_number+'What logical rack number configuration do you want?\n> ')).lower().strip()
    with open('ip_list.csv', "r") as f1:
        for line in f1:
            if line.startswith(logical_rack_number):
                rack_name = next(f1).strip()
                rack_location = next(f1).strip()
                configuration_ip_address = next(f1).strip()
                subnet_mask = next(f1).strip()
                default_gateway = next(f1).strip()
                break
        f1.close()
    return [rack_name,rack_location,contact_name,configuration_ip_address,default_gateway,subnet_mask,target_ip_address,new_pdu,connected_rack,logical_rack_number]

'''Main menu'''
if __name__ == "__main__":
    first_run = False
    user_confirmation = ''
    prompt = ''
    rack_name = ''
    rack_location = ''
    contact_name = ''
    configuration_ip_address = ''
    default_gateway = ''
    subnet_mask = ''
    logical_rack_number = ''
    target_ip_address = ''
    indexer = []
    new_pdu = False
    connected_rack = ''

    # Clears terminal for clean interface
    clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear_screen()

    run_loop = True
    while run_loop == True :
        clear_screen()
        print(f"{TEXT_COLOURS.OKGREEN}\nYou are connected to : {TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING}{target_ip_address} | {connected_rack}\n{TEXT_COLOURS.ENDC}")
        print(f"{TEXT_COLOURS.OKGREEN}The rack configuration you want is :\nLogical Rack :{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {logical_rack_number}{TEXT_COLOURS.ENDC}\n")
        print(f"{TEXT_COLOURS.OKGREEN}IP address :{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {configuration_ip_address}{TEXT_COLOURS.ENDC}")
        print(f"{TEXT_COLOURS.OKGREEN}Subnet Mask :{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {subnet_mask}{TEXT_COLOURS.ENDC}")
        print(f"{TEXT_COLOURS.OKGREEN}Default Gateway :{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {default_gateway}{TEXT_COLOURS.ENDC}\n")
        print(f"{TEXT_COLOURS.OKGREEN}PDU Name :{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {rack_name}{TEXT_COLOURS.ENDC}")
        print(f"{TEXT_COLOURS.OKGREEN}Location / Pod:{TEXT_COLOURS.ENDC}{TEXT_COLOURS.WARNING} {rack_location}\n{TEXT_COLOURS.ENDC}")
        prompt = str(input(prompt+'1. Select the target PDU\n2. Power Options\n3. PDU Options\n4. Exit Program\n> ')).lower().strip()
        if prompt == '1':
            clear_screen()
            indexer.clear()
            indexer = pdu_configuration_finder()
            rack_name = indexer[0]
            rack_location  =  indexer[1]
            contact_name =  indexer[2]
            configuration_ip_address =  indexer[3]
            default_gateway =  indexer[4]
            subnet_mask =  indexer[5]
            target_ip_address =  indexer[6]
            new_pdu =  indexer[7]
            connected_rack = indexer[8]
            logical_rack_number = indexer[9]
        elif prompt == '2':
            clear_screen()
            power_options(target_ip_address)
        elif prompt == '3':
            clear_screen()
            hardware_configuration_options(target_ip_address,configuration_ip_address,rack_name,rack_location,contact_name,default_gateway,subnet_mask,new_pdu)
        elif prompt == '4':
            runtime = False
            clear_screen()
            print("******************************\n PROGRAM IS SHUTTING DOWN!\n******************************\n\n")
            time.sleep(1)
            clear_screen()
            sys.exit()