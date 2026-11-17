"""Shared Groq chat client for EXA teacher conversations."""
import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings


logger = logging.getLogger('roadmap.admin')


class GroqClientError(RuntimeError):
    pass


class GroqClient:
    API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    DEFAULT_MODEL = 'openai/gpt-oss-120b'
    FALLBACK_MODEL = 'openai/gpt-oss-120b'

    @classmethod
    def _dotenv_value(cls, variable):
        env_file = Path(settings.BASE_DIR) / '.env'
        try:
            for line in env_file.read_text(encoding='utf-8').splitlines():
                entry = line.strip()
                if not entry or entry.startswith('#'):
                    continue
                if entry.startswith('export '):
                    entry = entry[7:].strip()
                name, separator, value = entry.partition('=')
                if separator and name.strip() == variable:
                    value = value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                        value = value[1:-1]
                    return value.strip()
        except OSError:
            return ''
        return ''

    @classmethod
    def _setting(cls, variable, default=''):
        return os.environ.get(variable, '').strip() or cls._dotenv_value(variable) or default

    @classmethod
    def _api_key(cls):
        return cls._setting('GROQ_API_KEY')

    @classmethod
    def teacher_model(cls):
        return cls._setting('GROQ_TEACHER_MODEL', cls.DEFAULT_MODEL)

    @classmethod
    def expert_model(cls):
        return cls._setting('GROQ_EXPERT_MODEL', cls.teacher_model())

    @classmethod
    def model_for(cls, panel):
        return cls.expert_model() if panel == 'expert' else cls.teacher_model()

    @classmethod
    def is_configured(cls):
        # Groq-issued API keys use the gsk_ prefix. Avoid showing Online for
        # placeholders or keys from another provider, which Groq rejects with 403.
        key = cls._api_key()
        return bool(key.startswith('gsk_') and len(key) > 20)

    @classmethod
    def _admin_log(cls, message):
        logger.error('%s', message)
        try:
            from .models import SystemAdminLog
            SystemAdminLog.objects.create(category='Groq API', message=message)
        except Exception:
            logger.exception('Could not persist Groq API failure to the admin log.')

    @classmethod
    def _request(cls, model, api_key, system_prompt, messages, max_tokens, timeout):
        payload_messages = [{'role': 'system', 'content': system_prompt}]
        payload_messages.extend(messages)
        payload = json.dumps({
            'model': model,
            'messages': payload_messages,
            'max_tokens': max_tokens,
            'temperature': 0.4,
        }).encode('utf-8')
        request = urllib.request.Request(
            cls.API_URL,
            data=payload,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read())
        reply = result.get('choices', [{}])[0].get('message', {}).get('content')
        if not isinstance(reply, str) or not reply.strip():
            raise GroqClientError('Groq returned an empty response.')
        return reply.strip()

    @classmethod
    def complete(cls, model, system_prompt, messages, *, max_tokens=1200, timeout=60):
        api_key = cls._api_key()
        if not api_key or not api_key.startswith('gsk_') or len(api_key) <= 20:
            cls._admin_log('GROQ_API_KEY is missing or is not a Groq-formatted key; teacher request was not sent.')
            raise GroqClientError('GROQ_API_KEY is missing or is not a valid Groq API key.')

        try:
            return cls._request(model, api_key, system_prompt, messages, max_tokens, timeout)
        except urllib.error.HTTPError as error:
            if error.code in (400, 403, 404) and model != cls.FALLBACK_MODEL:
                cls._admin_log(f'Groq rejected configured teacher model {model} (HTTP {error.code}); retrying with the supported fallback.')
                try:
                    return cls._request(
                        cls.FALLBACK_MODEL, api_key, system_prompt, messages, max_tokens, timeout,
                    )
                except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as fallback_error:
                    cls._admin_log(f'Groq fallback request failed: {type(fallback_error).__name__}.')
                    raise GroqClientError('Teacher is offline right now. Try again soon.') from None
            cls._admin_log(f'Groq API returned HTTP {error.code} for the teacher request.')
            if error.code == 403:
                raise GroqClientError('Groq rejected the API key or account access (HTTP 403). Check GROQ_API_KEY and Groq account access.') from None
            raise GroqClientError('Groq is offline right now. Try again soon.') from None
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, GroqClientError) as error:
            cls._admin_log(f'Groq teacher request failed: {type(error).__name__}.')
            raise GroqClientError('Groq is offline right now. Try again soon.') from None
