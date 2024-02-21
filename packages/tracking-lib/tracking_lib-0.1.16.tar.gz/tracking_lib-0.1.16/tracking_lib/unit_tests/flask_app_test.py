import os
import sys
import pytest
from tracking_lib.adapters.pubsub import PubSubAdapter
from tracking_lib.config import Config
from tracking_lib.models.transaction_status_update import TransactionStatusUpdate
from tracking_lib.transaction import Transaction
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to PATH
sys.path.append(parent_dir)


app = Flask(__name__)


def interactor_runc():
    # print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
    return Transaction.read_transaction_id()


@app.route("/success")
def hello_world_success():
    Transaction.init(Config())
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME")
    return jsonify(message=tr_id)


@app.route("/failure")
def hello_world_failure():
    Transaction.init(Config())
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    Transaction.set_transaction_status(
        src_event_name="AN_SRC_EVENT_NAME",
        status="FAILURE",
        error_message="some_error_message",
    )
    return jsonify(message=tr_id)


@app.route("/no_transaction_id")
def hello_world_no_transaction_id():
    Transaction.init(Config())
    tr_id = interactor_runc()
    Transaction.set_transaction_status(
        src_event_name="AN_SRC_EVENT_NAME",
        status="FAILURE",
        error_message="some_error_message",
    )
    return jsonify(message=tr_id)


# Test client fixture
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Unit test
def test_hello_world_success(client):
    with patch.object(
        TransactionStatusUpdate, "set_status_failure", new=MagicMock()
    ) as mock_method:
        response = client.get("/success")
        data = response.get_json()
        mock_method.assert_not_called()
        assert response.status_code == 200
        assert data["message"] == "123456"

    TransactionStatusUpdate.to_dict = MagicMock(return_value="a_dict")
    with patch.object(
        PubSubAdapter, "publish_to_control_channel", new=MagicMock()
    ) as mock_method:
        response = client.get("/success")
        data = response.get_json()
        mock_method.assert_called_once_with("a_dict", "TRANSACTION_STATUS_UPDATE")
        assert response.status_code == 200
        assert data["message"] == "123456"


def test_hello_world_failure(client):
    with patch.object(
        TransactionStatusUpdate, "set_status_failure", new=MagicMock()
    ) as mock_method:
        response = client.get("/failure")
        data = response.get_json()
        mock_method.assert_called_once_with("some_error_message")
        assert response.status_code == 200
        assert data["message"] == "123456"

    TransactionStatusUpdate.to_dict = MagicMock(return_value="a_dict")
    with patch.object(
        PubSubAdapter, "publish_to_control_channel", new=MagicMock()
    ) as mock_method:
        response = client.get("/failure")
        data = response.get_json()
        mock_method.assert_called_once_with("a_dict", "TRANSACTION_STATUS_UPDATE")
        assert response.status_code == 200
        assert data["message"] == "123456"


def test_hello_world_no_transaction_id(client):
    with patch.object(
        TransactionStatusUpdate, "set_status_failure", new=MagicMock()
    ) as mock_method:
        response = client.get("/no_transaction_id")
        data = response.get_json()
        mock_method.assert_not_called()
        assert response.status_code == 200
        assert data["message"] is None

    TransactionStatusUpdate.to_dict = MagicMock(return_value="a_dict")
    with patch.object(
        PubSubAdapter, "publish_to_control_channel", new=MagicMock()
    ) as mock_method:
        response = client.get("/no_transaction_id")
        data = response.get_json()
        mock_method.assert_not_called()
        assert response.status_code == 200
        assert data["message"] is None
