from unittest.mock import patch, MagicMock

import os, sys
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to PATH
sys.path.append(parent_dir)

from tracking_lib.transaction import Transaction
from tracking_lib.config import Config
from tracking_lib.models.transaction_status_update import TransactionStatusUpdate
from tracking_lib.adapters.pubsub import PubSubAdapter

# Unit test
def test_set_transaction_status_success():
    Transaction.init(Config())
    Transaction.read_transaction_id = MagicMock(return_value="123456")
    with patch.object(TransactionStatusUpdate, 'set_status_failure', new=MagicMock()) as mock_method:
        Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME")
        mock_method.assert_not_called()

    TransactionStatusUpdate.to_dict = MagicMock(return_value='a_dict')    
    with patch.object(PubSubAdapter, 'publish_to_control_channel', new=MagicMock()) as mock_method:
        Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME")
        mock_method.assert_called_once_with('a_dict', 'TRANSACTION_STATUS_UPDATE')    

def test_set_transaction_status_failure():
    Transaction.init(Config())
    Transaction.read_transaction_id = MagicMock(return_value="123456")
    with patch.object(TransactionStatusUpdate, 'set_status_failure', new=MagicMock()) as mock_method:
        Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME", status="FAILURE", error_message="some_error_message")
        mock_method.assert_called_once_with("some_error_message")

    TransactionStatusUpdate.to_dict = MagicMock(return_value='a_dict')    
    with patch.object(PubSubAdapter, 'publish_to_control_channel', new=MagicMock()) as mock_method:
        Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME", status="FAILURE", error_message="some_error_message")
        mock_method.assert_called_once_with('a_dict', 'TRANSACTION_STATUS_UPDATE')    
