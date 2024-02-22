from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException

class WatsonAssistantService:
    def __init__(self, apikey, version, url, assistant_id):
        authenticator = IAMAuthenticator(apikey)
        self.assistant = AssistantV2(version=version, authenticator=authenticator)
        self.assistant.set_service_url(url)
        self.assistant_id = assistant_id

    def create_session(self):
        response = self.assistant.create_session(assistant_id=self.assistant_id).get_result()
        return response.get('session_id')

    def delete_session(self, session_id):
        self.assistant.delete_session(assistant_id=self.assistant_id, session_id=session_id)

    def send_message(self, session_id, message):
        try:
            response = self.assistant.message(
                assistant_id=self.assistant_id,
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': message,
                    'options': {
                        'return_context': True
                    }
                }
            ).get_result()
            return response
        except ApiException as e:
            if e.code == 404 and e.message == 'Invalid Session':
                print('Session timed-out', session_id)
                raise

    def update_context_variable(self, session_id, variable_name, value):
        try:
            response = self.assistant.message(
                assistant_id=self.assistant_id,
                session_id=session_id,
                input={'message_type': 'text', 'text': '', 'options': {'return_context': True}},
                context={
                    'skills': {
                        'main skill': {
                            'user_defined': {
                                variable_name: value
                            }
                        }
                    }
                }
            ).get_result()
            return response['context']['skills']['main skill'].get('user_defined', {})
        except ApiException as e:
            if e.code == 404 and e.message == 'Invalid Session':
                print('Session timed-out', session_id)
                raise
    
    def get_context_variables(self, session_id):
        response=self.send_message(session_id=session_id, message='')
        # process response to get context variable (from "context.skills.main skill.user_defined")
        context=response['context']['skills']['main skill'].get('user_defined', {})
        return context
