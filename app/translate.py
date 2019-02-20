from google.cloud import translate
from flask_babel import _
from flask import current_app

def translate_text(text, dest_language):
	if 'GOOGLE_APPLICATION_CREDENTIALS' not in current_app.config or not current_app.config['GOOGLE_APPLICATION_CREDENTIALS']:
		return _('Error: the translation service is not configured.')
	translate_client = translate.Client()

	translation = translate_client.translate(text, target_language=dest_language)
	return translation

