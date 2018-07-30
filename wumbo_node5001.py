# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 12:15:00 2018

@author: sukhe
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 15:39:05 2018

@author: Abhinav
"""

#--------------------------------------------MINING BLOCKCHAINS--------------------------------
import os
os.chdir('D:\Shiz\Blockchain\Blockchain\WumboCoin')        
from blockchain import Blockchain 
from flask import Flask,jsonify,request #For web applications and returning messages in Postman respectively 
import requests # Catch the right nodes, older nodes have been synced
from uuid import uuid4 #Create a random unique address for nodes

#Creating a web-app
app = Flask(__name__)

#Creating a node address for its port (5000)
node_add= str(uuid4()).replace('-','') #UUID FORMAT HAS -, which needs to be avoided

#Creating a blockchain
bc = Blockchain()
#Mining a new block
@app.route('/mine_block',methods=['GET'])  #URL IS 127.0.0.1:5000 by default which is followed by /mine_block(user defined  url)
def mine_block():
    prev_block = bc.getLastBlock()  #Retrieves last block from blockchain
    prev_proof = prev_block['proof']         #Retrieves nonce of the last block
    proof = bc.workProof(prev_proof) #Returns new nonce from previous nonce
    last_hash = bc.hashFunction(prev_block)  #Returns hash function of the previous block
    #bc.addTransaction(sender=node_add,receiver='Vikhyat',amt=2) #Implementing add transaction method
    block = bc.createBlock(proof,last_hash) #Creates a block from nonce and previous hash (2 out of 4 main properties of block)
    #Response message and properties of block in postman.
    res = {'Message': 'Block mined successfully',
           'index':block['index'],
           'timestamp':block['timestamp'],
           'proof':block['proof'],
           'prev_hash':block['prev_hash'],
           'transactions':block['transactions']
           }
    return jsonify(res), 200


#Retrieving all blocks in the chain
    
@app.route('/get_all_blocks', methods = ['GET'])
def allBlocks():
    
    #Displays blockchain and length
    res = {'blockchain': bc.chain,
           'blocks': len(bc.chain)}
    return jsonify(res), 200

#Check if blockchain is valid
@app.route('/validity', methods = ['GET'])
def isValid():
    
    validChain = bc.checkValidBlockChain(bc.chain)
    if(validChain):
        res = {'message':'It\'s all OK, It\'s all Good!'}
    else:
        res = {'message': 'Chain doesn\'t seem valid'}
        
    return jsonify(res),200

#Adding new transactions to blockchain
@app.route('/new_transaction',methods = ['POST']) 
def addTransaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    if not all (key in json for key in transaction_keys):
        return 'Elements missing in transaction', 400
    index= bc.addTransaction(json['sender'],json['receiver'],json['amount'])
    res={'message': f'Transaction added to block {index}'}
    return jsonify(res),201

#Connecting new nodes
@app.route('/connect_nodes',methods=['POST'])
def nodeConnect():
    json=request.get_json()
    nodes = json.get('nodes') #Registering multiple nodes
    #Check if the request made is valid
    if nodes is None:
        return 'Number of nodes = number of fucks I give about your favorite djent band',400
    for node in nodes:
        bc.addNode(node)
    res= {'message':'Nodes connected.',
          'nodes': list(bc.nodes)}
    return jsonify(res),201

#Replacing blockchain by the longest blockchain
@app.route('/chain_validity',methods=['GET'])
def chainValidity():
    isChainReplaced = bc.chainChecker()
    if(isChainReplaced):
        res={'message':'Blocks were different, boy. But It\'s all ok now',
             'new_chain': bc.chain}
    else:
        res={'message':'Chain is fine'}
    return jsonify(res),200
app.run(host='0.0.0.0', port =5001)   #Runs the application



