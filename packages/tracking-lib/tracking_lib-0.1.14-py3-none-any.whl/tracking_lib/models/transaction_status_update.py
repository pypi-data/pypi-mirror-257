import time

class TransactionStatusUpdate():

    def __init__(self, transaction_id, src_event_name, downstream_service):
        self.transaction_id=transaction_id
        self.src_event_name=src_event_name
        self.status='SUCCESS'
        self.error_message=None
        self.event_time=int(time.time())
        self.event_name="TRANSACTION_STATUS_UPDATE"
        self.downstream_service=downstream_service

    def set_status_failure(self, error_message):
        self.status='FAILURE'
        self.error_message=error_message

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "src_event_name": self.src_event_name,
            "status": self.status,
            "error_message": self.error_message,
            "event_time": self.event_time,
            "event_name": self.event_name,
            "downstream_service": self.downstream_service
        }

    
    