import json
from google.cloud import pubsub_v1

class PubSubAdapter():

    def __init__(self, project_id=None, topic_id=None):
        self.project_id = project_id
        self.topic_id = topic_id
        if project_id and topic_id:
            self.publisher = pubsub_v1.PublisherClient()
        else:
            self.publisher = None    

    def get_topic_path(self):
        return self.publisher.topic_path(project=self.project_id, topic=self.topic_id)

    def publish_to_control_channel(self, message, event_type):
        if not self.project_id or not self.topic_id:
            print(f"control message: {message}, event_type:{event_type}", flush=True)
            return

        topic_path = self.get_topic_path()
        _data = json.dumps(message).encode('utf-8')
        # print(f'control message: {_data}', flush=True)
        future = self.publisher.publish(topic=topic_path, data=_data,
                                        event_type=event_type)  # message attributes
        print(f"PubSub result: {future.result()}", flush=True)  # block the code until the message is sent
