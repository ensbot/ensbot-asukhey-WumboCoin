# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 00:53:37 2018

@author: sukhe
"""
#Install following package
#request =2.18.4 ( pip install requests==2.18.4)
#_____________________________________CRYPTOCURRENCY__________________________
from blockchain import Blockchain
import datetime
import hashlib
import json
from flask import Flask,jsonify,request #Request module connects nodes in decentralized model 
import requests # Catch the right nodes, older nodes have been synced
from uuid import uuid4
from urllib.parse import urlparse 


#Decentralize Blockchain 
#Transactions make blockchain cryptocurrency
#Consesus makes sure that 

#Consesus problem : tackling it by replacing a shorter chain with longer chain