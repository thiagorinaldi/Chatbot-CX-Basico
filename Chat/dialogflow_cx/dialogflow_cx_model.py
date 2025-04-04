class DialogflowCXModel():
    def __init__(self, project_id, location, language_code, agent_id, session_id) -> None:
        self.project_id = project_id
        self.location = location
        self.language_code = language_code
        self.agent_id = agent_id
        self.session_id = session_id