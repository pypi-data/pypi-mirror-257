import os
from .watsonx_assistant_service import WatsonAssistantService
from ibm_cloud_sdk_core.api_exception import ApiException


# Initialise watsonx assistant service
from .constants import ENV_WATSONX_ASSISTANT_ID, ENV_WATSONX_ASSISTANT_APIKEY, WATSONX_ASSISTANT_VERSION, WATSONX_ASSISTANT_SERVICE_URL
waApiKey = os.environ.get(ENV_WATSONX_ASSISTANT_APIKEY)
waAssistantId = os.environ.get(ENV_WATSONX_ASSISTANT_ID)
waVersion = WATSONX_ASSISTANT_VERSION
waServiceUrl = WATSONX_ASSISTANT_SERVICE_URL

waService=WatsonAssistantService(waApiKey, waVersion, waServiceUrl, waAssistantId)

historyTemplate="""
Question: {nlq}
SQL: {sql}
"""

def createNewSession():
    session_id=waService.create_session()
    return session_id

def getSessionIntent(session_id):
    """
    Method to get the current intent of the session. This would help identify conversation's intent in case of follow-up question.
    """
    context=waService.get_context_variables(session_id)
    if context.get('history') is not None:
        current_intent=context['history'].get('intent', '')
    return current_intent

def getSessionHistoryTemplate(session_id):
    """
    This method retrieves contextual session memory and build template.
    """
    context=waService.get_context_variables(session_id)
    # Build historyTemplate to be used in prompt as previous conversation
    history=context.get('history', None)
    if history is None:
        return
    joinedNlq=';'.join(str(question) for question in history.get('questions', []))
    return historyTemplate.format(nlq=joinedNlq, sql=history.get('sql',''))

def getSessionHistoryVariables(session_id):
    """
    This method retrieves and returns contextual session memory variables.
    """
    context=waService.get_context_variables(session_id)
    return context

def clearSessionHistory(session_id):
    return waService.update_context_variable(session_id, 'history', None)
        
def deleteSession(session_id):
    return waService.delete_session(session_id)

def addContextForSession(nlq, sql, intent, session_id):
    """
    This method stores the user's question along with the generated SQL query to the session memory.
    Also capturing the intent of the session.
    """
    context=waService.get_context_variables(session_id)

    # Check if history already exists in context
    if context.get('history') is not None:
        questions=context['history'].get('questions',[])
        questions.append(nlq)
        current_intent=context['history'].get('intent', intent)
    else:
        questions = [nlq]
        current_intent=intent
    
    history={
        'questions': questions,
        'sql': sql,
        'intent': current_intent
    }
    return waService.update_context_variable(session_id, 'history', history)

def markAwaitFeedbackForSession(nlq, intent, session_id):
    """
    This method sets awaiting feedback flag True and
    also captures required details to resume after feedback received
    """
    context=waService.get_context_variables(session_id)
    history=context.get('history')

    history={**history, 'awaiting_feeback': True, 'next_question': nlq, 'next_intent': intent}
    
    return waService.update_context_variable(session_id, 'history', history)

def processFeedbackReceived(feedbackResponse, session_id):
    """
    This method is to process the feedback received from user for the given session.

    If feedbackResponse:
        yes OR anything else, clear the whole history attribute.
        no,  clear awaiting_feeback, next_question and next_intent.
        
    Returns 'next_question' attribute value to use as current nlq.
    """
    context=waService.get_context_variables(session_id)
    history=context.get('history', None)
    nlq=''
    if history is not None and history.get('awaiting_feeback', False) is True:
        nlq=history['next_question']
        if feedbackResponse.lower() == 'no':
            history={
                'questions': history['questions'],
                'sql': history['sql']
            }
        else:
            history={
                'intent': history['next_intent']
            }

    waService.update_context_variable(session_id, 'history', history)

    return nlq