# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,  # length of the chain plus 1
            'timestamp': time(),  # use the time function
            # ref to the current transactions of the blockchain
            'transactions': self.current_transactions,
            'proof': proof,  # the proof provided to the function
            # the hash supplied to the function or the one derived from previous block
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)

        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        string_object = json.dumps(block, sort_keys=True)

        # Create the block_string
        block_string = string_object.encode()

        # Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()
        # Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # encode blockstring and proof to genereate a guess
        guess = f"{block_string}{proof}".encode()
        # hash the guess
        guess_hash = hashlib.sha256(guess).hexdigest()
        # return True or False
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
# handle non json responses
    values = request.get_json()
    # check that the required fields are in the posted data
    required_fields = ['proof', 'id']
    if not all(k in values for k in required_fields):
        response = {'message': "Missing Values"}
        return jsonify(response), 400

    # get the submitted proof from the values data
    submitted_proof = values.get('proof')
    # determine if the proof is valid
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True).encode()

    if blockchain.valid_proof(last_block_string, submitted_proof):
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(submitted_proof, previous_hash)

        # reward the miner for work
        blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200
    # otherwise
    else:
        # send a message stating that proof was invalid or already submitted
        response = {'message': 'Proof was invalid or already submitted'}

        return jsonify(response), 200


    # # Pull data from the post
    # data = request.get_json()
    # # Get the current block string
    # block_string = json.dumps(blockchain.last_block, sort_keys=True).encode()

    # # TODO: check if it's the first correct POW
    # # if first_correct_POW:
    # #     return jsonify({'message': "Correct proof already submitted"}), 400

    # # check that `proof` and `id` are present in the post
    # if data.proof and data.id:
    #     # check if the proof is correct
    #     if blockchain.valid_proof(block_string, data.proof):
    #         # previous hash
    #         previous_hash = blockchain.hash(blockchain.last_block)
    #         # forge new block
    #         block = blockchain.new_block(data.proof, previous_hash)
    #         # reward the proof
    #         blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    #         # return success message
    #         return jsonify({'message': "New Block Forged"}), 200
    # return jsonify({'message': "Proof incorrect"}), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # Return the chain and its current length
        'length': len(blockchain.chain),  # length
        'chain': blockchain.chain  # chain
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return json(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # get the values in json format
    values = request.get_json()
    # check that the required fields exist
    required_fields = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required_fields):
        response = { 'message': 'Error Missing values' }
        return jsonify(response), 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    # set the response object with a message that the transaction will be added at the index
    response = { 'message': f'Transaction will be added to Block {index}'}
    # return the response
    return jsonify(response), 201

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
