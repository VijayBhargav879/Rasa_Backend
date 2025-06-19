from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ActionFallbackChatGPT(Action):
    def name(self) -> Text:
        return "action_fallback_chatgpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message.get("text")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0.5,
                messages=[
                    {"role": "system", "content": "You are a helpful and accurate assistant for renewable energy awareness."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception:
            reply = ""
        print("🔵 Sending to ChatGPT:", user_input)
        print("🟢 ChatGPT reply:", reply)
        dispatcher.utter_message(text=reply)
        return []
