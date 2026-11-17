"""Shared, key-safe Claude API client for EXA's AI features."""
import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
import uuid

from django.conf import settings


logger = logging.getLogger('roadmap.admin')


class ClaudeClientError(RuntimeError):
    pass


class ClaudeResponseError(ValueError):
    pass


class ClaudeClient:
    API_URL = 'https://api.anthropic.com/v1/messages'
    API_VERSION = '2023-06-01'
    TEACHER_MODEL = 'claude-haiku-4-5-20251001'
    EVALUATION_MODEL = 'claude-sonnet-5'

    @classmethod
    def _api_key(cls):
        key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
        if key:
            return key

        env_file = Path(settings.BASE_DIR) / '.env'
        try:
            for line in env_file.read_text(encoding='utf-8').splitlines():
                entry = line.strip()
                if not entry or entry.startswith('#'):
                    continue
                if entry.startswith('export '):
                    entry = entry[7:].strip()
                name, separator, value = entry.partition('=')
                if separator and name.strip() == 'ANTHROPIC_API_KEY':
                    value = value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                        value = value[1:-1]
                    return value.strip()
        except OSError:
            return ''
        return ''

    @classmethod
    def is_configured(cls):
        return bool(cls._api_key())

    @classmethod
    def _admin_log(cls, message, exc_info=False):
        logger.error('%s', message, exc_info=exc_info)
        try:
            from .models import SystemAdminLog
            SystemAdminLog.objects.create(category='Claude API', message=message)
        except Exception:
            # Logging must not obscure the original provider error, especially before migrations.
            logger.exception('Could not persist Claude API failure to the admin log.')

    @classmethod
    def complete(cls, model, system_prompt, messages, *, max_tokens=1200, timeout=60):
        """Send a Claude Messages request and return its text blocks as one string."""
        api_key = cls._api_key()
        if not api_key:
            cls._admin_log('ANTHROPIC_API_KEY is missing; Claude request was not sent.')
            raise ClaudeClientError('Claude API key is not configured.')

        payload = json.dumps({
            'model': model,
            'max_tokens': max_tokens,
            'system': system_prompt,
            'messages': messages,
        }).encode('utf-8')
        request = urllib.request.Request(
            cls.API_URL,
            data=payload,
            headers={
                'x-api-key': api_key,
                'anthropic-version': cls.API_VERSION,
                'content-type': 'application/json',
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read())
            text = '\n'.join(
                block.get('text', '') for block in body.get('content', [])
                if block.get('type') == 'text'
            ).strip()
            if not text:
                raise ClaudeClientError('Claude returned an empty response.')
            return text
        except urllib.error.HTTPError as error:
            cls._admin_log(f'Claude API returned HTTP {error.code} for model {model}.')
            raise ClaudeClientError(f'Claude API request failed (HTTP {error.code}).') from None
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            cls._admin_log(f'Claude API request failed for model {model}: {type(error).__name__}.')
            raise ClaudeClientError('Claude API request failed. Please try again soon.') from None
        except ClaudeClientError as error:
            cls._admin_log(f'Claude API response failed for model {model}: {error}')
            raise

    @classmethod
    def parse_json(cls, response_text):
        """Parse and centrally validate that a provider response is a JSON object."""
        try:
            result = json.loads(response_text)
        except (TypeError, json.JSONDecodeError) as error:
            cls._admin_log('Claude returned invalid JSON.')
            raise ClaudeResponseError('Claude returned invalid JSON.') from error
        if not isinstance(result, dict):
            cls._admin_log('Claude returned JSON that was not an object.')
            raise ClaudeResponseError('Claude response must be a JSON object.')
        return result

    @classmethod
    def transcribe_audio_file(cls, audio_path):
        """Keep the existing speech-to-text provider call inside the shared AI client module."""
        key = os.environ.get('OPENAI_API_KEY', '').strip()
        if not key:
            cls._admin_log('OPENAI_API_KEY is missing; audio transcription was not sent.')
            raise ClaudeClientError('Video transcription is unavailable because OPENAI_API_KEY is not configured.')
        boundary = '----EXA' + uuid.uuid4().hex
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        parts = [
            f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n'.encode(),
            f'--{boundary}\r\nContent-Disposition: form-data; name="response_format"\r\n\r\njson\r\n'.encode(),
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode(),
            audio_data,
            f'\r\n--{boundary}--\r\n'.encode(),
        ]
        request = urllib.request.Request(
            'https://api.openai.com/v1/audio/transcriptions',
            data=b''.join(parts),
            headers={
                'Authorization': f'Bearer {key}',
                'Content-Type': f'multipart/form-data; boundary={boundary}',
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read())
            transcript = result.get('text', '').strip()
            if not transcript:
                raise ClaudeClientError('Speech-to-text returned an empty transcript.')
            return transcript
        except urllib.error.HTTPError as error:
            cls._admin_log(f'Speech-to-text API returned HTTP {error.code}.')
            raise ClaudeClientError(f'Video transcription failed (HTTP {error.code}).') from None
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            cls._admin_log(f'Speech-to-text request failed: {type(error).__name__}.')
            raise ClaudeClientError('Video transcription request failed. Please try again soon.') from None
