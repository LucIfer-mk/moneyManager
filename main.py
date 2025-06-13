import json
import os
import tkinter as tk

from login import login
from dashboard import dashboadr

loginstate = False

if __name__ == "__main__":
   if loginstate == True:
    dashboadr()
   else:
     login()
        

