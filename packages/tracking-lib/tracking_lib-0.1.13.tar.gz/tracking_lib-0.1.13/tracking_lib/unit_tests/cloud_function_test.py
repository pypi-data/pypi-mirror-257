
import os, sys
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to PATH
sys.path.append(parent_dir)

import time
import requests
import subprocess
import pytest
from tracking_lib.transaction import Transaction

def interactor_runc():
    #print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
    return Transaction.read_transaction_id()

def hello_world(request):
    request_args = request.args
    print(request_args)
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    return {"message": f"{tr_id}"}

@pytest.fixture(scope='module')
def server():
    # Start the server
    server = subprocess.Popen(['functions-framework', '--target=hello_world', f'--source={current_dir}/cloud_function_test.py', '--port=8000'])
    time.sleep(5)  # Wait for the server to start
    yield server
    # Teardown : Stop the server
    server.terminate()

def test_server(server):
    # Send a request to the server
    response = requests.get('http://0.0.0.0:8000')
    print(response.json())
    # Check that the server responded with status code 200
    assert response.status_code == 200

    # Check the content of the response
    assert response.json() == {"message":"123456"}
    





    

