import os
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
from requests import session


def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()
    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    return response


def detect_intent_texts(project_id, session_id, message, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print(f"Query text: {response.query_result.query_text}")
    print(
        f"Detected intent: {response.query_result.intent.display_name} "
        f"(confidence: {response.query_result.intent_detection_confidence})\n"
    )
    print(f"Fulfillment text: {response.query_result.fulfillment_text}\n")


load_dotenv()
session_id = os.getenv("TELEGRAM_USER_ID")
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
message = "Привет"
language_code = "ru"
detect_intent_texts(project_id, session_id, message, language_code)
