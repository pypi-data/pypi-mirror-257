import os, sys
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to PATH
sys.path.append(parent_dir)

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
import pytest
from tracking_lib.transaction import Transaction

app = FastAPI()

def interactor_runc():
    #print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
    return Transaction.read_transaction_id()

@app.get('/')
async def read_root(request: Request):
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    return {"message": f"{tr_id}"}

# Test client fixture
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Unit test
def test_read_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "123456"}
