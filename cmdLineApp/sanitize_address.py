import re




def sanitize(text):
    return re.sub(r'[^\w\s-]', '_', text).replace(' ', '_')


