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
def auth():
    def getSecret(secretName):
        keyVaultName = "BadgeIT"
        KVUri = f"https://{keyVaultName}.vault.azure.net"

        clientId = "be6b9aff-51c0-49b9-a97a-dd6ad807727a"
        tenantId = "36da45f1-dd2c-4d1f-af13-5abe46b99921"
        clientSecret = "SJr8Q~XfWkGNBsvl7GdKssTD9kbzQrr4MBiGAalA"

        credential = ClientSecretCredential(tenantId, clientId, clientSecret)
        client = SecretClient(vault_url=KVUri, credential=credential)

        retrieved_secret = client.get_secret(secretName)
        
        return retrieved_secret.value

    session = requests.Session()
    
    user = getSecret("ServiceNowUserName")
    print(user)
    passW = getSecret("ServiceNowPassword") 
    print(passW)
    session.auth = (user, passW)
    session.headers.update = {"Content-Type": "application/json",
               "Accept": "application/json"}
    
auth()