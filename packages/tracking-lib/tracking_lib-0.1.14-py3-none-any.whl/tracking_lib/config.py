
class Config:

    def __init__(self, downstream_service=None, control_channel_project_id=None, control_channel_topic_id=None):
        self.downstream_service = downstream_service
        self.control_channel_project_id = control_channel_project_id
        self.control_channel_topic_id = control_channel_topic_id

    