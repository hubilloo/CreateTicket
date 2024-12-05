import re
from selenium import webdriver
from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import time
from webbrowser import get
import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


cache = "C:\Temp"
cacheManager = DriverCacheManager(root_dir=cache)
driver = Service(EdgeChromiumDriverManager(cache_manager=cacheManager).install())

def auth():
    def getSecret(secretName):
        keyVaultName = "BadgeIT"
        KVUri = f"https://{keyVaultName}.vault.azure.net"

        clientId = "e8047582-72ec-4c3b-8b8c-041439c6d49c"
        tenantId = "36da45f1-dd2c-4d1f-af13-5abe46b99921"
        clientSecret = "eSA8Q~Ry8ey0W8kYYwLfkA54IKH-WqiIxd9EScu2"

        credential = ClientSecretCredential(tenantId, clientId, clientSecret)
        client = SecretClient(vault_url=KVUri, credential=credential)

        retrieved_secret = client.get_secret(secretName)
        
        return retrieved_secret.value

    session = requests.Session()
    
    user = getSecret("ServiceNowUserName")

    passW = getSecret("ServiceNowPassword") 
 
    session.auth = (user, passW)
    session.headers.update = {"Content-Type": "application/json",
               "Accept": "application/json"}
    return session

def submitData(req_code):
    snowURL = "https://deloitteus.service-now.com"
    session = auth()
    #print(session)
    reqNum = req_code
    #print(reqNum)
    reqFor = userName.get()
    sysID = (getSysID(snowURL, session, reqNum))
    #print(sysID)
    updateTicket(snowURL, session, sysID, reqNum, reqFor)

def updateTicket(snowURL, session, sysID, reqNum, reqFor):
    if not sysID:
        print("No SysID Provided")
        return
    url = f"{snowURL}/api/now/table/sc_request/{sysID}"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    param = {
        "requested_for": reqFor
    }

    response = session.put(url, headers=headers, json=param)
    if response.status_code == 200:
        print("SUCCESS")
    else:
        print("FAIL")

def getSysID(snowURL, session, reqNum):
    url= f"{snowURL}/api/now/table/sc_request"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    param = {
        "number": reqNum,
        "sysparam_fields": "sys_id"

    }
    response = (session.get(url, headers=headers, params=param))
    #print(response.json())
    if response.status_code == 200:
        result = response.json().get("result", [])
        if result:
            return result[0].get("sys_id")
        

def snowEdge():
    sTime = datetime.now()
    Total = []
    chromeopt = webdriver.EdgeOptions()
    #chromeopt.add_argument("--headless=new")
    chromeopt.add_argument("start-maximized")
    chromeopt.add_argument('--no-sandbox')
    chromeopt.add_argument("--log-level=3")
    chrome = webdriver.Edge(service=driver, options=chromeopt)
    chrome.set_window_position(-2000,0)
    #chrome = webdriver.Edge(options=chromeopt)
    action = ActionChains(chrome)
    #Navigate to URL
    url = "https://deloitteus.service-now.com/sp?id=sc_cat_item&sys_id=c4feb0f34f07b600f7a9cf5d0210c70d&table=sc_cat_item"
    chrome.get(url)
    
    
    # # #Login
    try:
        WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        try:
            time.sleep(3)
            chrome.find_element(By.ID, "onetrust-accept-btn-handler").click()
            #CookiesPrmpt
            #print("Cookie Click--------------------------------------------------------------------------------------------------")
            
        except:
            print("No Cookie Found")

        #Req For
        testPath = "/html/body/div[1]/section/main/div[2]/div/sp-page-row/div/div[2]/span[2]/div/div/div/div/div[1]/div[3]/form/div/sp-variable-layout/div[1]/div/div/div[1]/div/span/span/div[2]/div"
        WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.XPATH,testPath)))
        reqFor = chrome.find_element(By.XPATH,testPath)
        action.move_to_element(reqFor).perform()
        reqFor.click()
        Input = "s2id_autogen11_search"
        reqForInput = chrome.find_element(By.ID, Input)
        reqForInput.send_keys("Guest user Employee") #Pass Req For User ---> infoList[4]
        time.sleep(1)
        reqForInput.send_keys(Keys.ENTER)
        


        #Location
        Input = "s2id_sp_formfield_Where_are_you_currently_located"
        office = chrome.find_element(By.ID, Input)
        action.move_to_element(office).perform()
        office.click()
        Input = "s2id_autogen12_search"
        officeInput = chrome.find_element(By.ID, Input)
        officeLoc = fromProcess.get()
        officeInput.send_keys(officeLoc) #Pass Office location
        time.sleep(1)
        officeInput.send_keys(Keys.ENTER)
        
        #Request Area
        Input = "s2id_sp_formfield_Please_select_request_area"
        rArea = chrome.find_element(By.ID, Input)
        action.move_to_element(rArea).perform()
        rArea.click()
        Input = "s2id_autogen2_search"
        rAreaInput = chrome.find_element(By.ID, Input)
        rAreaInput.send_keys("Wipe") #Pass Request Area
        time.sleep(1)
        rAreaInput.send_keys(Keys.ENTER)
        
        #Device Carrier
        Input = "s2id_sp_formfield_Deloitte_device_carrier"
        dCarrier = chrome.find_element(By.ID, Input)
        action.move_to_element(dCarrier).perform()
        dCarrier.click()
        
        Input = "s2id_autogen3_search"
        dCarrierInput = chrome.find_element(By.ID, Input)
        dCarrierInput.send_keys(mobileCarrier.get()) #Pass Device Carrier
        time.sleep(1)
        dCarrierInput.send_keys(Keys.ENTER)
        
        #Compliance Check - Req Field
        Input = "s2id_sp_formfield_If_compliance_is_selected_what_is_the_compliance_issue"
        compCheck = chrome.find_element(By.ID, Input)
        action.move_to_element(compCheck).perform()
        compCheck.click()
        Input = "s2id_autogen4_search"
        compCheckInput = chrome.find_element(By.ID, Input)
        compCheckInput.send_keys("Personal Device") #Pass Comp Check
        time.sleep(1)
        compCheckInput.send_keys(Keys.ENTER)
        ### End of Required Input ###
      
        #Device MTN
        Input = "sp_formfield_Mobile_Telephone_Number"
        deviceMTN = chrome.find_element(By.ID, Input)
        action.move_to_element(deviceMTN).perform()
        deviceMTN.click()
        deviceMTN.send_keys(Keys.SPACE) #Pass MTN
        #Device IMEI
        Input = "sp_formfield_IMEI_or_ESN_Hex_Number"
        deviceIMEI = chrome.find_element(By.ID, Input)
        action.move_to_element(deviceIMEI).perform()
        deviceIMEI.click()
        deviceIMEI.send_keys(IMEI.get()) #Pass IMEI
        # #Emp Personal Email 
        # Input = "sp_formfield_Employees_Personal_Email_Address"
        # empEmail = chrome.find_element(By.ID, Input)
        # action.move_to_element(empEmail).perform()
        # empEmail.click()
        # empEmail.send_keys("johndoe@test.com") #Pass email

        #Device Wipe Status
        Input = "s2id_sp_formfield_Wipe_Status"
        compCheck = chrome.find_element(By.ID, Input)
        action.move_to_element(compCheck).perform()
        compCheck.click()
        Input = "s2id_autogen10_search"
        compCheckInput = chrome.find_element(By.ID, Input)
        compCheckInput.send_keys("Wiped/Reset to factory defaults") #Pass Wipe Status
        time.sleep(1)
        compCheckInput.send_keys(Keys.ENTER)
        #Device MTN Status
        Input = "s2id_sp_formfield_MTN_Status"
        compCheck = chrome.find_element(By.ID, Input)
        action.move_to_element(compCheck).perform()
        compCheck.click()
        Input = "s2id_autogen7_search"
        compCheckInput = chrome.find_element(By.ID, Input)
        compCheckInput.send_keys(mtnStatus.get()) #Pass MTN Stat
        time.sleep(1)
        compCheckInput.send_keys(Keys.ENTER)
        #Device reason for not wiping
        Input = "s2id_sp_formfield_Reason_for_Not_Wiping_Data"
        compCheck = chrome.find_element(By.ID, Input)
        action.move_to_element(compCheck).perform()
        compCheck.click()
        Input = "s2id_autogen6_search"
        compCheckInput = chrome.find_element(By.ID, Input)
        # select2-result-label-38
        # compCheckInput.select_by_visible_text('SDHD 10 day hold')

        compCheckInput.send_keys("SDHD 10 day hold") #Pass Reason
        time.sleep(1)
        compCheckInput.send_keys(Keys.ENTER)

        #Device remote wipe sent
        Input = "s2id_sp_formfield_Remote_Wipe_Sent"
        compCheck = chrome.find_element(By.ID, Input)
        action.move_to_element(compCheck).perform()
        compCheck.click()
        Input = "s2id_autogen9_search"
        compCheckInput = chrome.find_element(By.ID, Input)
        compCheckInput.send_keys("No") #Pass No
        time.sleep(1)
        compCheckInput.send_keys(Keys.DOWN)
        time.sleep(1)
        compCheckInput.send_keys(Keys.ENTER)


        print("Form Complete")
        eTime = datetime.now()
        print("Process Time: ", eTime - sTime)

        #Submit
        Input = "/html/body/div[1]/section/main/div[2]/div/sp-page-row/div/div[2]/span[2]/div/div/div/div/div[1]/div[4]/div/div/button"
        dCarrier = chrome.find_element(By.XPATH, Input)
        action.move_to_element(dCarrier).perform()
        dCarrier.click()
        try:
            alert_element = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/span")))
            
            alert_text = alert_element.text
            
            full_text = alert_text[8:18]
            
        except Exception as e:
            print("Error")
        req_code = re.search(r'REQ\d+', full_text).group()
        #print(req_code) 
        submitData(req_code)
        messagebox.showerror("Ticket Number", req_code)
        #fromProcess.set("Select Office")
        
        mobileCarrier.set("Select Carrier")
        
        #selectReason.set("Select reason")
        
        #mtnStatus.set("Select MTN Status")
        
        userName.delete(0,'end')
        IMEI.delete(0,'end')

        get().open("https://deloitteus.service-now.com/sc_request.do?sysparm_query=number="+ req_code)

    
    except Exception as error:
        print("Error: ", error)



root = tk.Tk()
root.title("Mobile Device - Create Ticket")

root.geometry("500x500")
root.resizable(False, False) 

 

frame = tk.Frame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)


# downloadReport = ctk.CTkButton(frame, text="Download Report", command=getReport)
# downloadReport.pack(pady=20, padx=10)



locLabel = tk.Label(frame, text="",font=("arial",30))
locLabel.pack()
offices = ['Aguascalientes_Avenida Guadalupe Gonzalez', 'Albany_111 Washington Avenue', 'ALBUQUERQUE-121 TIJERAS NE', 'ALEXANDRIA - 1725 DUKE ST.', 'Alexandria_6363 Walker Lane', 'ANCHORAGE - 645 G STREET', 'ANNAPOLIS JUNC-135 NAT BUS PKY', 'ANNAPOLIS JUNCTION_306 SENTINE', 'Annapolis Junction_420 National Business Parkway', 'Arlington Heights_601 W. Campus Dr.', 'ARLINGTON-1401 SOUTH CLARK ST.', 'ARLINGTON-1919 NORTH LYNN', 'ARLINGTON-4250 NORTH FAIRFAX', 'ARLINGTON-4301 N FAIRFAX DRIVE', 'ARLINGTON-KINGSTOWNE VILLAGE', 'ARLINGTON_1101 WILSON BOULEVRD', 'Arlington_1777 N. Kent Street', 'Arlington_1919 North Lynn', 'Arlington_2200 Crystal Drive', 'ATLANTA - 100 PEACHTREE ST.', 'Atlanta_1000 Abernathy Road', 'Atlanta_1230 Peachtree Street, NE', 'Atlanta_191 Peachtree Street, NE', 'Austin - 1101 Capital Of Texas Highway', 'Austin_1009 South Congress Avenue', 'Austin_1609 Centre Creek Drive', 'Austin_500 West 2nd Street', 'Austin_701 Brazos Street', 'Austin_7601 Southwest Parkway', 'Austin_7700 West Parmer Lane', 'Baltimore_500 E.Pratt Street', 'Baltimore_7111 Security Boulevard', 'BANGALORE HULKUL', 'Baton Rouge_100 North Street', 'Beit Shemesh_Yigal Alon 1', 'Bellevue_1285 122nd Avenue NE', 'BENGALURU - MIDWAY', 'BENGALURU-MUNEKOLALU VILLAGE', 'Bengaluru_Bannerghatta Road', 'Bengaluru_Block 7, 77 Town Centre', 'Bengaluru_Block A 77 Town Center', 'Bengaluru_Block B Salarpuria', 'Bengaluru_Block C1 Building DivyaSree Technopolis', 'Bengaluru_Block C2 Building DivyaSree Technopolis', 'Bengaluru_Ecoworld Bellandur Sarjapur', 'Bengaluru_Prestige Falcon Tower(Valence)', 'Bengaluru_Prestige Falcon Tower(Velocity)', 'BENGALURU_PRIMECO TOWERS', 'Bengaluru_Sattva Eminence', 'Bengaluru_Sector 2 HSR Layout', 'BENGALURU_SOMASANDRA PAYLA', 'Bengaluru_Varthur Hobli(Block A)', 'Bengaluru_Varthur Hobli(Block B)', 'Bethesda_6555 Rock Spring Drive', 'Birmingham_420 North 20th Street', 'Boca Raton_1800 North Military Trail', 'Boise_800 West Main Street', 'BOSTON - CLARENDON ST.', 'BOSTON - CLARENDON ST.(DNU)', 'Boston_115 Federal Street', 'Boston_200 Berkeley Street', 'BOULDER - 4001 DISCOVERY DRIVE', 'BRISTOL_636 SHELBY STREET', 'Buffalo_6500 Sheridan Drive', 'CAMP HILL - 100 SENATE AVE', 'CAMP HILL-200 CORPORATE CNTR', 'Camp Hill_300 Corporate Center Drive', 'CARLSBAD - 2325 FARADAY AVE', 'Carson City_1717 College Parkway', 'CEDAR RAPIDS-4840 N RIVER BLVD', 'CENTENNIAL_9195 E. MINERAL AVE', 'Chantilly_15049 Conference Center Drive', 'Chantilly_15059 Conference Center Drive', 'CHARLESTON-1012 KANAWHA BLVD', 'CHARLESTON_4700 MACCORKLE AVE', 'CHARLOTTE-227 WEST TRADE ST', 'CHARLOTTE-4135 SO STREAM BLVD', 'Charlotte_650 S.Tryon Street', 'CHARLOTTE_650 S.TRYON STREET', 'Chennai_Citi Centre', 'Chennai_CSIR Road Taramani', 'Chennai_NO. 8/17 Sunnyside', 'Cheyenne_1950 Bluegrass Circle', 'CHICAGO - 111 SOUTH WACKER DR', 'CHICAGO - 550 WEST VAN BUREN', 'CHICAGO_111 EAST WACKER DRIVE', 'Chicago_111 South Wacker Drive', 'Chicago_566 West Adams Street', 'CINCINNATI - 50 W FIFTH STREET', 'Cincinnati_50 W Fifth Street', 'Cleveland_127 Public Square', 'COLORADO SPRINGS-555 E PEAK AV', 'Colorado Springs_90 S. Cascade Avenue', 'COLUMBUS - 330 RUSH ALLEY', 'Columbus_330 Rush Alley', 'CONCORD-7 EAGLE SQUARE', 'DALLAS - ROSS AVENUE (DC)', 'Dallas_2200 Ross Avenue', 'Dallas_717 N. Harwood Street', 'DARIEN_17 OLD KINGS HIGHWAY SO', 'Dayton_711 E.Monument Avenue', 'DEERFIELD-DNU', 'Delhi_Gurgaon_Plot No. 15', 'Delhi_Gurugram_Ambience Corporate Towers - II', 'DELHI_GURUGRAM_FRONTLINE BUS.', 'DELHI_GURUGRAM_TOWER C BLDG 8', 'DENVER 1400 16TH STREET', 'DENVER-601 EAST 18TH STREET', 'Denver_1455 16th Street, Suite 307', 'Denver_1601 Wewatta Street', 'Des Moines_699 Walnut', 'DETROIT_1001 WOODWARD AVE', 'Detroit_1001 Woodward Ave', 'DEU-Senden', 'DOWNERS GROVE_1901 BUTTERFIELD', 'Eilat_The City Center, P.O.B 583', 'ELKRIDGE - 6810 DEERPATH ROAD', 'ENGLEWOOD_6900 SOUTH PEORIA ST', 'Escazu Village_Bldg 1', 'FALLS CHURCH-5111 LEESBURG', 'FALLS CHURCH-5111 LEESBURG PK', 'FALLS CHURCH-5201 LEESBURG PK', 'FALLS CHURCH-5205 LEESBURG PK', 'Falls Church_2941 Fairview Park Drive', 'Falls Church_5275 Leesburg Pike', 'Fort Worth_301 Commerce Street', 'FOSTER CITY - 950 TOWER LANE', 'Frankfort_306 W. Main Street', 'Fresno_5250 North Palm Avenue', 'FT. LAUDERDALE', 'GILBERT_161 EAST RIVULON BLVD', 'Gilbert_300 E. Rivulon Boulevard', 'Gilbert_310 East Rivulon Blvd', 'Glen Mills_1 Braxton Way', 'Glendale_1520 Flower Street', 'Glendale_550 N. Brand Blvd', 'GRAND RAPIDS_37 OTTAWA AVENUE', 'Grand Rapids_37 Ottawa Avenue', 'Greensboro_303 Pisgah Church Road', 'Guadalajara_Amado Nervo #2200', 'Guadalajara_Calle Avenida Moctezuma No. 144', "Haifa_5 Ma'aleh Hashichrur", 'HARRISBURG-3600 VARTAN WAY', 'Harrisburg_30 North Third Street', 'Hartford_185 Asylum Street', 'HATTIESBURG-5912 U S HWY 49', 'Helena_350 North Last Chance Gulch', 'Hermitage_4022 Sells Drive', 'Hermitage_4026 Sells Drive', 'HICKORY - 200-1ST AVE NW', 'Honolulu_733 Bishop Street', 'Honolulu_999 Bishop Street', 'Horsham_5 Walnut Grove Drive', 'Houston_1111 Bagby Street', 'HUNTSVILLE_3414 GOVERNORS DR', 'Huntsville_3414 Governors Drive SW', 'HYDERABAD', 'HYDERABAD - BLOCK A', 'HYDERABAD - BLOCK B', 'HYDERABAD - BLOCK C', 'Hyderabad - Block E', 'HYDERABAD - BLOCK F', 'HYDERABAD - BLOCK G', 'HYDERABAD - BLOCK K', 'HYDERABAD - BLOCK L', 'HYDERABAD - BLOCK N', 'HYDERABAD-DELOITTE UNIVERSITY', 'HYDERABAD_BLOCK H', 'Hyderabad_Deloitte Tower 1', 'Hyderabad_Deloitte Tower 1', 'Hyderabad_Deloitte Tower 2', 'Hyderabad_Deloitte Tower 3', 'HYDERABAD_ISPROUT BUSINESS CEN', 'IND-Bengaluru Bannerghatta', 'IND-Bengaluru Block C', 'IND-Bengaluru Hulkul', 'IND-Bengaluru Somasandra', 'IND-Chennai CitiCenter', 'IND-Chennai Crest Building', 'IND-Chennai Sunnyside', 'IND-Gurgaon', 'IND-Hyderabad', 'IND-Kolkata', 'IND-Mumbai', 'IND-Pune', 'INDIANAPOLIS-151 N.DELAWARE ST', 'Indianapolis_111 Monument Circle', 'Indore_Level 6 Vijay Nagar', 'Inglewood_900 District Drive', 'IRVING-6363 N STATE HWY 161', 'Jacksonville_50 North Laura Street', 'Jericho_2 Jericho Plaza', 'JERSEY CITY_15 EXCHANGE PLACE', 'Jersey City_Harborside Plaza 10', "Jerusalem_3 Kiryat Ha'Mada, Har Hotzvim Tower", 'Kansas City_1100 Walnut Street', 'KOCHI_NH BYPASS PADIVATTOM', 'Kolkata_4A Abanindra Nath Thakur Sarani', 'LA CROSSE - 505 KING STREET', 'Lake Mary_1001 Heathrow Park Lane', 'Lake Mary_901 International Parkway', 'Lansing_106 West Allegan', 'Las Vegas_3883 Howard Hughes Parkway', 'Las Vegas_8474 Rozita Lee Avenue', 'Lexington Park_22454 Three Notch Road', 'LINTHICUM HEIGHTS-901 ELKRIDGE', 'LITTLE ROCK - 111 CENTER ST', 'Little Rock_400 W. Capitol Avenue', 'LOS ANGELES - LAX', 'Los Angeles_21255 Burbank Boulevard', 'Los Angeles_555 West Fifth Street', 'Louisville_220 West Main Street', 'Lucknow_Levana Cyber Heights Gomti Nagar', 'MADISON-433 W WASHINGTON AVE', 'Madison_834 East Washington Avenue', 'MAITLAND_2405 LUCIEN WAY 1', 'Manhattan Beach_1600 Rosecrans Avenue', 'MCLEAN - 1751 PINNACLE DRIVE', 'McLean_7900 Tysons One Place', 'Mechanicsburg_200 Sterling Parkway', 'Mechanicsburg_300 Sterling Parkway', 'Memphis_6075 Poplar Avenue', 'MEX-Aguascalientes', 'MEX-Guadalajara', 'MEX-Monterrey', 'MEX-Querétaro', 'MIAMI_600 BRICKELL AVENUE', 'Miami_600 Brickell Avenue', 'Midland_3320 Ridgecrest Drive', 'Milwaukee_555 East Wells Street', 'Minneapolis_50 South 6th Street', 'Monterey_70 Garden Court', 'Monterrey_1008 and 958 Calle Hidalgo West', 'Morristown_M Station East', 'MORRISVILLE-3020 CARRINGTON MI', 'Mumbai_Hiranandini Business Park', 'Mumbai_Winchester', 'Nashville_100 Centerview Drive', 'Nashville_1033 Demonbreun Street', 'Nashville_333 Commerce Street', 'Nazareth_Marj Ibn Amer Street 9', 'New Brunswick_65-75 Church Street', 'New Brunswick_90-94 Albany', 'NEW CASTLE_2 PENNS WAY', 'New Orleans_701 Poydras Street', 'NEW YORK - 115 BROADWAY', 'NEW YORK - 1633 BROADWAY', 'NEW YORK - 1633 BROADWAY IPB', 'NEW YORK - 25 BROADWAY', 'NEW YORK - 489 FIFTH AVENUE', 'New York_1221 Avenue of the Americas', 'NEW YORK_140 BROADWAY', 'New York_30 Rockefeller Plaza', 'New York_330 Hudson Street', 'Newtown Square - 3809 West Chester Pike', 'NORTH CHARLESTON_2120 N BLVD', 'North Kingstown_100 Commerce Park Road', 'OAKLAND - 1111 BROADWAY', 'OAKLAND - 180 GRAND AVENUE', 'OAKLAND - 180 GRAND AVENUE', 'Oklahoma_City_100 N Broadway', 'Olympia_111 Market Street NE', 'Olympia_711 South Capitol Way', 'Omaha_1100 Capitol Avenue', 'OMAHA_1100 CAPITOL AVENUE', 'Orange County_695 Town Center Drive', 'ORLANDO-200 SOUTH ORANGE (DNU)', 'PALO ALTO_431 FLORENCE STREET', 'PANAMA CITY-2908 THOMAS DRIVE', 'PARSIPPANY - 100 KIMBALL DRIVE', 'PENSACOLA - 2065 AIRPORT BLVD', 'PENSACOLA-2114 AIRPORT BLVD', 'Peoria_101 SW Adams Street', 'Philadelphia_1700 Market Street', 'Pittsburgh_1 PPG Place', 'PLANO - 7700 WINDROSE AVENUE', 'PLEASANTON_6200 STONERIDGE MAL', 'Pleasanton_6200 Stoneridge Mall Road', 'PORTLAND_1125 NW COUCH STREET', 'Portland_1125 NW Couch Street', 'Portland_630 NW 14th Avenue', 'Princeton_500 College Road East', 'PROVIDENCE - 10 CHARLES ST.', 'Pune_Grant Road, Kharadi (B1)', 'Pune_Sky Vista, Viman Nagar', 'Queretaro_Avenida 5 de Febrero No.1351 (Ceiba)', 'Queretaro_Avenida 5_de_Febrero_No.1351(Tab. & Ced)', 'Quincy_Three Batterymarch Park', 'RAANANA_HAPNINA ST 8', 'Raleigh_150 Fayetteville Street Mall', 'Raleigh_621 Hillsborough Street', 'RED BANK_2-10 BROAD ST.', 'Reno_200 S. Virginia Street', 'RESTON', 'RESTON_11700 PLAZA AMERICA DRI', 'RICHMOND - 919 EAST MAIN ST', 'Richmond_901 East Byrd Street', 'ROSWELL_1801 OLD ALABAMA ROAD', 'SACRAMENTO-8810 CAL CENTER DR', 'Sacramento_2329 2399 Gateway Oaks Drive', 'Sacramento_980 9th Street', 'Saint Louis_100 South 4Th Street', 'Salem_117 Commercial Street', 'SALEM_2755 PENCE LOOP SE', 'Salt Lake City_111 South Main Street', 'San Antonio_14100 San Pedro', 'SAN ANTONIO_310 S. ST. MARY ST', 'SAN DIEGO-8910 UNIVERSITY CTR', 'SAN DIEGO_12830 EL CAMINO REAL', 'San Diego_12830 El Camino Real', 'San Diego_2448 Historic Decatur Rd', 'SAN DIEGO_2811 NIMITZ BLVD', 'San Diego_2811 Nimitz Blvd', 'San Diego_350 Tenth Avenue', 'SAN FRANCISCO-555 MISSION ST', 'SAN FRANCISCO-MARKET STREET', 'San Francisco_1100 Sansome Street', 'San Francisco_555 Mission Street', 'San Jose_225 West Santa Clara', 'San Juan_350 Carlos Chardon Avenue', 'SANTA ANA - 1 MACARTHUR PLACE', 'SANTA FE-215 LINCOLN AVENUE', 'Santa Fe_150 Washington Avenue', 'Scott AFB_715 Seibert Road', 'Seattle - 100 South King Street', 'SEATTLE_1015 2ND AVENUE', 'Seattle_1015 2nd Avenue', 'Seattle_821 Second Avenue', 'SEATTLE_837 NORTH 34TH STREET', 'Senden_Robert-Bosch-Str. 1D', 'Springfield_201 East Adams', 'Springfield_One West Old State Capitol Plaza', 'Stamford - 333 Ludlow Street', 'Stamford_695 East Main Street', 'SUMMIT NJ (DNU)', 'Suwanee_300 Satellite Blvd', 'Tallahassee_215 South Monroe Street', 'Tampa_201 North Franklin Street', 'Tel Aviv_1 Azrieli Center', 'Tel Aviv_3 Azrieli Center', 'Tel Aviv_Nirim 8', 'Tempe_100 S. Mill Avenue', 'Tempe_100 S. Mill Avenue', 'TIRAT HACARMEL_MEDONE', 'TULSA-100 SOUTH CINCINNATI AVE', 'Tulsa_6100 South Yale Avenue', 'US OFFSHORE/EXPATS (HERMITAGE)', 'USA-Arlington', 'USA-Arlington Heights', 'USA-Atlanta', 'USA-Austin 500 West 2nd', 'USA-Austin 7601 Southwest PW', 'USA-Baltimore', 'USA-Birmingham', 'USA-Boca Raton', 'USA-Boise', 'USA-Boston', 'USA-Charlotte', 'USA-Chicago', 'USA-Cincinnati', 'USA-Cleveland', 'USA-Colorado Springs', 'USA-Columbus', 'USA-Costa Mesa', 'USA-Dallas', 'USA-Davenport', 'USA-Dayton', 'USA-Denver', 'USA-Denver 1455 16th Street', 'USA-Denver 1601 Wewatta', 'USA-Des Moines', 'USA-Detroit', 'USA-Fort Worth', 'USA-Fresno', 'USA-Gilbert', 'USA-Glen Mills', 'USA-Grand Rapids', 'USA-Harrisburg', 'USA-Hartford', 'USA-Hermitage', 'USA-Honolulu', 'USA-Houston', 'USA-Huntsville', 'USA-Indianapolis', 'USA-Jacksonville', 'USA-Jericho', 'USA-Jersey City', 'USA-Kansas City', 'USA-Lake Mary', 'USA-Las Vegas', 'USA-Los Angeles', 'USA-Louisville', 'USA-Memphis', 'USA-Mexico', 'USA-Miami', 'USA-Midland', 'USA-Milwaukee', 'USA-Milwaukee 555 East Wells', 'USA-Minneapolis', 'USA-Morristown', 'USA-Nashville', 'USA-New Orleans', 'USA-New York 1221 Ave. of Amer', 'USA-New York 30 Rockefeller', 'USA-New York 330 Hudson', 'USA-Omaha', 'USA-Philadelphia', 'USA-Phoenix', 'USA-Pittsburgh', 'USA-Pleasanton', 'USA-Portland', 'USA-Princeton', 'USA-Raleigh', 'USA-Richmond', 'USA-Rochester', 'USA-Sacramento', 'USA-Salt Lake City', 'USA-San Antonio', 'USA-San Diego', 'USA-San Francisco', 'USA-San Jose', 'USA-San Juan', 'USA-Seattle 1015 Second Avenue', 'USA-Seattle 821 Second Ave', 'USA-St. Louis', 'USA-Stamford', 'USA-Tallahassee', 'USA-Tampa', 'USA-Tempe', 'USA-Tulsa', 'USA-Washington', 'USA-Westlake', 'USA-Wichita', 'USA-Williamsville', 'VIRGINIA BEACH - 295 BENDIX RD', 'Vizag_Waltair Main Road', 'WALNUT CREEK - 2033 N MAIN ST', 'WALTHAM - 1000 WINTER STREET', 'WASHINGTON DC_701 PENNSLYVANIA', 'Washington_1299 Pennsylvania Avenue NW', 'Washington_1299 Pennsylvania Avenue NW', 'WESTLAKE VILLAGE_2625 TOWNSGAT', 'Westlake_2501 Westlake Parkway', 'Wichita_1960 N. Innovation Blvd.', 'WOODLAND HILLS', 'Woodland Hills_21550 Oxnard Street'] 
fromProcess = ttk.Combobox(frame,values=offices,width = 300) 
fromProcess.pack(pady=10, padx=10)
# 'ARLINGTON-1919 NORTH LYNN
# fromProcess.set("Hermitage_4022 Sells Drive") 
fromProcess.set("Hermitage_4022 Sells Drive") 
mobileCarrier = ttk.Combobox(frame,values=[" ","T-MOBILE","VERIZON","AT&T"],width = 300)
mobileCarrier.pack(pady=10,padx=10)
mobileCarrier.set("Select Carrier")
selectReason = ttk.Combobox(frame,values=["Upgrade","Separation"],width = 300) 
selectReason.pack(pady=10,padx=10)
selectReason.set("Separation")
mtnStatus = ttk.Combobox(frame,values=["Cancel the MTN","Keep MTN active (i.e. device upgrade)", "Release"],width = 300)
mtnStatus.pack(pady=10,padx=10)
mtnStatus.set("Cancel the MTN")
usernameLabel = tk.Label(frame, text="",font=("arial",30))
usernameLabel.configure(text="USERNAME")
usernameLabel.pack()

usernameLabel2 = tk.Label(frame, text="",font=("arial",8))
usernameLabel2.configure(text="Verify username in DCD or ticket will create under Guest User Employee")
usernameLabel2.pack()

userName = tk.Entry(frame,width = 300)
userName.pack(pady=10,padx=10)
imeiLabel = tk.Label(frame, text="",font=("arial",30))
imeiLabel.configure(text="IMEI")
imeiLabel.pack()
IMEI = tk.Entry(frame,width = 300)
IMEI.pack(pady=10,padx=10)

submitbutton = tk.Button(frame, text="Submit",command=snowEdge)
submitbutton.pack(pady=10,padx=10)




root.mainloop()