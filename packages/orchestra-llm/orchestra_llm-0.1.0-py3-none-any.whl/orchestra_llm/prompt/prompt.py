import os, inspect
import xml.etree.ElementTree as ET
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from langchain.prompts import MessagesPlaceholder

class Prompter:
    def __init__(self):
        self.dir = os.path.abspath(os.path.dirname(self.get_caller_path()))

    def get_caller_path(self):
        frame = inspect.stack()[2]
        caller_path = frame.filename
        return caller_path

    def load(self, pathfile, schema, **kwargs):
        tree = ET.parse(os.path.join(self.dir, pathfile))
        root = tree.getroot()
        chat_prompt = []
        for child in root:
            element_name = child.tag
            if element_name == 'system-prompt':
                chat_prompt.append(
                    SystemMessagePromptTemplate.from_template(child.text.strip())
                )
            elif element_name == 'human-prompt':
                chat_prompt.append(
                     HumanMessagePromptTemplate.from_template(child.text.strip())
                )
            elif element_name == "message-placeholder":
                chat_prompt.append(
                    MessagesPlaceholder(variable_name=child.get("variable_name"))
                )
        chat_prompt = ChatPromptTemplate.from_messages(chat_prompt)
        return chat_prompt