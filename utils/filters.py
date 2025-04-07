supported_symbols = '''ёйцукенгшщзхъфывапролджэячсмитьбю'''+'''ёйцукенгшщзхъфывапролджэячсмитьбю'''.upper()

def filter_ascii(text):
    filtered_text = ''.join([i if ord(i) < 128 or i in supported_symbols else '' for i in text])
    return filtered_text if len(filtered_text.replace(' ', "")) > 0 else 'NO KEY TABLE'
