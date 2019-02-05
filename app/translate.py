from google.cloud import translate
from flask_babel import _
from app import app

def translate_text(text, dest_language):
	if 'GOOGLE_APPLICATION_CREDENTIALS' not in app.config or not app.config['GOOGLE_APPLICATION_CREDENTIALS']:
		return _('Error: the translation service is not configured.')
	translate_client = translate.Client()

	translation = translate_client.translate(text, target_language=dest_language)
	return translation['translatedText']

