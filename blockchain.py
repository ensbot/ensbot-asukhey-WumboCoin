# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:45:20 2018

@author: Abhinav 
"""

#Install flask- A web dev framework in "anaconda prompt"    
#pip install Flask==0.12.2

#____________________________________________________________________________________
#PACKAGES     

import datetime #Block needs a timestamp
import hashlib  #Hash the blocks
import json    #Retrieve JSON attributes
from flask import Flask,jsonify #For web applications and returning messages in Postman respectively
import requests # Catch the right nodes, older nodes have been synced
from uuid import uuid4
from urllib.parse import urlparse 

 
#_____________________ _______________________________________________________________
     
#PROGRAMMING TIPS: Since blockchain is a huge application , 
    #that involves decentralized network connections, always code in CLASSES and not FUNCTIONS


#----------------------------------------------BUILD BLOCKCHAIN------------------------------
    
    # Attention: Proof is Nonce in this case
class Blockchain:
    
    #Init method is important, similar to constructor , to initialize variables.
    def __init__(self):
        self.chain = [] #Initialize Blockchain variable- This will hold different blocks.
        self.transactions =[] #Transactions make blockchain cryptocurrency. They need to be before createBlock function else chain will be initialized without transactions.
        self.createBlock(proof = 1, prev_hash='0')
        #METHOD ABOVE is GENESIS Block generator that will accept:
        #proof i.e sr.no (which will be 1 since genesis block is the first block)
        #and previous_hash as parameters. 
        #NOTE: prev_hash accepts string variables because SHA256 only accepts encoded strings.
        self.nodes=set()
    
    #Method to create block, that is declared above    
    def createBlock(self, proof,prev_hash):
        
        #Dictionary to hold following variables of a block: sr_no, prev_hash, hash, data
        block={
                'index': len(self.chain) +1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'prev_hash': prev_hash,
                'transactions': self.transactions}
        #After adding the transactions in the block, list should be empty
        self.transactions =[]
        #Add block to the blockchain
        self.chain.append(block)
        return block
        
    def getLastBlock(self):
        return self.chain[-1]   #-1 is the last element in a list
    
    #This method defines, problem statement and the solution to the problem
    def workProof(self, prev_proof):
        new_proof = 1
        #To check if proof is valid
        isProof = False
        
        while (isProof is False):
            #Defining problem- check if current proof has four 0s in the start. 
            #If the statement is true, isProof = True
            
            #Function below produces a hashcode by adding previous proof and new proof
            #Operation should be ASYMMETRICAL
                #Symmetrical => a+b (cause a+b = b+a)
                #Asymmetrical => a-b (a-b != b-a)
            #STEP 1:
            #PRoduce a hashcode
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            
            #STEP 2: Check if hashcode has 4 0s: 
            #MIND WELL , its [:4] for it checks elements from 0 to 3 (excluding 4)
            if(hash_operation[:4] == '0000'):
                isProof = True
            else:
                new_proof +=1   #Increment new proof
            #End of while loop
        return new_proof #Return proof (NONCE)
    
    #End of function
    
    
    def hashFunction(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest() 
    
    #Check if Blockchain is valid by Checking:
        #if prev_hash property of a block is similar to hash of previous block
        # Proo(Nonce) is valid   
        
    def checkValidBlockChain(self, chain):
        #Variable initializations before while loop
        prev_block = chain[0]   #First block in BlockChain
        block_index = 1 #Block index in the dictionary. Starts with 1
        
        #Here we go with the iterations BABAY!!!!!!
        while(block_index <len(chain)):
            block = chain[block_index]
            
            #Check COndition 1!
            #Don't get confused with this line, read carefully:
                #If Block of previous hash is not equal to hash of previous block.
            if(block['prev_hash']!= self.hashFunction(prev_block)):
                return False
            
            #Check Condition 2
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            #Check first 4 characters are 0000
            if (hash_operation[:4]!='0000'):
                return False
            #increment in loop
            prev_block = block
            block_index +=1
        #If everything is valid
        return True
    
        #Method to add transaction: It'll hold 3 important elements- Sender,Reciever, Amount
    def addTransaction(self,sender, receiver,amt):
        self.transactions.append({'sender':sender,
                                  'receiver':receiver,
                                  'amount': amt})
        #Need to append the transaction in the latest block that'll be mined. For this we need the last block mined
        prev_block = self.getLastBlock()
        return prev_block['index'] +1 #Returns index of the new block
    #NOTE: FOR THE FUNCTION ABOVE, BLOCK NEEDS TO BE MINED FIRST TO ADD TRANSACTIONS.
    
    #Will accept node and its address
    def addNode(self,address):
        #Parse the address of the node
        parsed_url=urlparse(address) #Parse url and retrieves a set of properties i.e protocol=http, netloc=ip address + port
        self.nodes.add(parsed_url.netloc) #add only netloc cause that's what we need
   #Solves the consesus problem i.e replacing a shorter chain with larger chain             
    def chainChecker(self): 
        nw=self.nodes #Network of all the nodes
        lc = None #Longest chain
        max_len=len(self.chain)
        for node in nw:
             res=requests.get(f'http://{node}/get_all_blocks')
             #Check if the chain retrieved from node is valid, Valid request returns 200 response
             if(res.status_code==200):
                 length= res.json()['blocks']
                 chain= res.json()['blockchain']

                 if length > max_len and self.checkValidBlockChain(chain):
                     max_len=length
                     lc=chain
        if lc:
            self.chain=lc
            return True
        return False

           

         

         