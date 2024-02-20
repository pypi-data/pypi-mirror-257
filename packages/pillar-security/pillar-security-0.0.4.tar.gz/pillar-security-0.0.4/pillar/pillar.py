import requests
import datetime
import importlib.metadata
import uuid
import logging
from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Optional
from contextlib import contextmanager
from packaging import version
from wrapt import wrap_function_wrapper

from .logging import Logger
from .hooks.openai import hook_chat_completions
from . import context_vars

@dataclass
class Report:
    block: bool

def _uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

class Pillar:
    _instance = None
    def __init__(self, url, app_id, api_key):
        if not _uri_validator(url):
            raise ValueError(f'Invalid url for pillar: {url}')
        self.url = url
        self.app_id = app_id
        self.api_key = api_key
        self.requests = requests.Session()
        self.requests.headers.update({
            'X-App-Id': app_id,
            'X-Api-Key': api_key,
        })
        self.logger =  Logger(self)

        if Pillar._instance is not None:
            logging.warning('Pillar was initialized more than once. If using streamlit, use st.cache_resource to cache the Pillar object.')
        else:
            Pillar._instance = self  # This also prevents the instance from being garbage collected
            self._initialize_hooks()

    def check_prompt(self, prompt: str, policy: str = 'default') -> Report:
        return self._check_prompt(prompt, policy)
    
    def _check_prompt(self, prompt: str, policy: str = 'default', role: str = 'user'):
        url = f'{self.url}/application/check_prompt'
        response = self.requests.post(url, json={            
            'session_id': context_vars.session_id.get() or str(uuid.uuid4()),
            'message': prompt,
            'policy': policy,
            'author': context_vars.user_id.get() or '',
            'role': role,
            'timestamp': datetime.datetime.now().isoformat()
        })
        if response.status_code != 200:
            raise RuntimeError(f'Unexpected status code {response.status_code} from pillar guard. {response.text}')
    
        return Report(block=response.json()['action'] == 'block')

    def check_response(self, response: str, policy: str = 'default'):
        url = f'{self.url}/application/check_response'
        message_id = context_vars.last_assistant_message_id.get()
        response = self.requests.post(url, json={            
            'id': message_id,
            'session_id': context_vars.session_id.get() or str(uuid.uuid4()),
            'message': response,
            'policy': policy,
            'author': 'assistant',
            'timestamp': datetime.datetime.now().isoformat()
        })
        if response.status_code != 200:
            raise RuntimeError(f'Unexpected status code {response.status_code} from pillar guard. {response.text}')
        return Report(block=response.json()['action'] == 'block')

    def check_tool_response(self, response: str, policy: str = 'default'):
        return self._check_prompt(response, policy, role='function')

    def _write(self, session_id: str, message: str, role: str, author: str, model: str, service: str):
        url = f'{self.url}/application/messages'
        message_id = str(uuid.uuid4())
        if role == 'assistant':
            context_vars.last_assistant_message_id.set(message_id)
        self.requests.post(url, json={
            'id': message_id,
            'message': message,
            'role': role,
            'author': author,
            'model': model,
            'service': service,
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    def _write_tool(self, name: str, description: str, parameters: dict):
        url = f'{self.url}/application/tools'
        self.requests.post(url, json={
            'name': name,
            'description': description,
            'parameters': parameters,
        })

    def _log(self, level, message):
        url = f'{self.url}/application/logs'
        try:
            self.requests.post(url, json={
                'level': level,
                'message': message,
                'timestamp': datetime.datetime.now().isoformat()
            })
        except Exception as e:
            logging.log(level, message)

    @contextmanager
    def session(self, user_id: Optional[str] = None, session_id: Optional[str] = None):
        if session_id is None:
            session_id = str(uuid.uuid4())

        session_id_token = context_vars.session_id.set(session_id)
        token_user_id = context_vars.user_id.set(user_id)
        try:
            yield
        finally:
            context_vars.session_id.reset(session_id_token)
            context_vars.user_id.reset(token_user_id)


    def _initialize_hooks(self):
        self._initialize_hooks_openai()

    def _initialize_hooks_openai(self):
        try:
            openai_version = version.parse(importlib.metadata.version('openai'))
        except importlib.metadata.PackageNotFoundError:
            return
        
        if openai_version < version.parse('1.0.0'):
            wrap_function_wrapper('openai', 'ChatCompletion.create', hook_chat_completions(self))
        else:
            wrap_function_wrapper('openai.resources.chat.completions', 'Completions.create', hook_chat_completions(self))


            