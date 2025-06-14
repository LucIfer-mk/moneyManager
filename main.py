import json

import tkinter as tk

from login import login
from dashboard import dashboadr

def get_login_data():
  with open("user_data.json", "r") as file:
    data = json.load(file)
    return data.get("logged_in")
  

if __name__ == "__main__":
   if get_login_data():
    dashboadr()
   else:
     login()
        

