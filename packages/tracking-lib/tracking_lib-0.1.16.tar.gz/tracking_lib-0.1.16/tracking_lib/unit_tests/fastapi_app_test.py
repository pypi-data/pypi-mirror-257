import os
import sys
import pytest
from tracking_lib.adapters.pubsub import PubSubAdapter
from tracking_lib.models.transaction_status_update import TransactionStatusUpdate
from tracking_lib.transaction import Transaction
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to PATH
sys.path.append(parent_dir)


app = FastAPI()


def interactor_runc():
    # print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
    return Transaction.read_transaction_id()


@app.get("/")
async def read_root(request: Request):
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    return {"message": f"{tr_id}"}


@app.get("/no_transaction_id")
async def read_no_transaction_id(request: Request):
    tr_id = interactor_runc()
    return {"message": tr_id}


# Test client fixture
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# Unit test
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "123456"}


def test_hello_world_no_transaction_id(client):
    with patch.object(
        TransactionStatusUpdate, "set_status_failure", new=MagicMock()
    ) as mock_method:
        response = client.get("/no_transaction_id")
        data = response.json()
        mock_method.assert_not_called()
        assert response.status_code == 200
        assert data["message"] is None

    TransactionStatusUpdate.to_dict = MagicMock(return_value="a_dict")
    with patch.object(
        PubSubAdapter, "publish_to_control_channel", new=MagicMock()
    ) as mock_method:
        response = client.get("/no_transaction_id")
        data = response.json()
        mock_method.assert_not_called()
        assert response.status_code == 200
        assert data["message"] is None
