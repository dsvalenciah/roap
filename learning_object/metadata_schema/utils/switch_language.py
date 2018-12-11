import gettext


class SwitchLanguage():
    def __call__(self, req, resp, resource, params):
        valid_langs = {
            'en_US': 'en_US',
            'es_CO': 'es_CO',
            'pt_BR': 'pt_BR'
        }
        value_lang_cookie = valid_langs.get(
            req.cookies.get('user_lang')) or 'es_CO'

        language = gettext.translation(
            'metadata_schema', '/code/locale', languages=[value_lang_cookie])

        req.context['user'] = {
            'language': language.gettext
        }
