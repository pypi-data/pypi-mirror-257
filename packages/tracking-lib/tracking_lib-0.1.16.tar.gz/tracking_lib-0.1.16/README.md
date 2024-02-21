# Overview
The tracking_lib is a python module that is used by the PA development team to orchestrate the control messages that are sent in the Control Channel. It uses the Web Frameworks' (Flask, FastAPI) feature to keep a state in the request lifecycle in order to maintain and communicate a transaction id among different services. The following section describes the supprted features.


# Features
- Create and store a Transaction id 
- Sent status messages for SUCCESS or FAILURE


# Installation
    pip install tracking-lib

# How to use it
    import os

    from tracking_lib.config import Config
    from tracking_lib.transaction import Transaction
    from flask import Flask, jsonify

    app = Flask(__name__)


    def interactor_runc():
        # print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
        return Transaction.read_transaction_id()


    @app.route("/")
    def hello_world_success():
        Transaction.init(Config(
             downstream_service="TVDI_CONFIGS_MANAGER",
            control_channel_project_id=os.getenv("CONTROL_CHANNEL_PROJECT_ID"),
            control_channel_topic_id=os.getenv("CONTROL_CHANNEL_TOPIC_ID")

        ))
        Transaction.set_transaction_id("123456")
        tr_id = interactor_runc()
        Transaction.set_transaction_status(src_event_name="AN_SRC_EVENT_NAME")
        return jsonify(message=tr_id)


