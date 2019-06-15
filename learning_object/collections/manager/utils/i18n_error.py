class ErrorTranslator():
    def __init__(self, translator):
      self._ = translator

    def i18n_error(self, errors):
        for key, value in errors.items():
            if isinstance(value, dict):
                self.i18n_error(value)
            else:
                str_errors = errors[key]
                for index_str_error in range(0, len(str_errors)):
                    str_errors[index_str_error] = self._(str_errors[index_str_error]) 

        return errors
