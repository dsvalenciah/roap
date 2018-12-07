import gettext


class SwitchLanguage():
    def __call__(self, req, resp, resource, params):
        value_lang_cookie = req.cookies.get('user_lang') or 'es_CO'

        language = gettext.translation(
            'login', '/code/locale', languages=[value_lang_cookie])

        req.context['language'] = language.gettext
