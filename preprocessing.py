import re
import quopri

def remove_non_words(text):
    sentences = text.split('\n')
    final_sentences = list()
    for sentence in sentences:
        if sentence == '' or sentence == '.':
            continue
        words = sentence.split()
        final_words = list()
        for w in words:
            if re.search(r'[^A-Za-z0-9#[]- \,\.\?\:\n]', w) is None:
                final_words.append(w)
        final_sentences.append(' '.join(final_words))
    return '\n'.join(final_sentences)


def add_periods(text):
    def get_replacement_caps(match):
        return f'.\n{match.group(0)[-1]}'
    def get_replacement_lower(match):
        return f' {match.group(0)[-1]}'
    text = re.sub(r'\n[A-Z0-9]', get_replacement_caps, text)
    text = re.sub(r'\n[a-z]', get_replacement_lower, text)
    text = re.sub(r'\ \.', '.', text)
    text = re.sub(r'\.\ ', '. ', text)
    text = re.sub(r'\.+', '.', text)
    return text


def remove_whitespace(text):
    text = text.strip()
    text = re.sub(r'[\r\n]+', '\n', text)
    text = re.sub(r'[\n\r]+', '\n', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n +', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\t+', '', text)
    text = text.strip()
    return text


def remove_links(text):
    text = re.sub(r'http\S+', 'HTTPS', text)
    return text


def remove_plain_text_special(text):
    def get_replacement_caps(match):
        return f'.\n{match.group(0)[-1]}'
    text = re.sub(r'=\n[A-Z0-9]', get_replacement_caps, text)
    text = re.sub(r'=\n\r[A-Z0-9]', get_replacement_caps, text)
    text = re.sub(r'=\r\n[A-Z0-9]', get_replacement_caps, text)
    text = re.sub(r'=\n', '', text)
    text = re.sub(r'=\n\r', '', text)
    text = re.sub(r'=\r\n', '', text)
    try:
        text = quopri.decodestring(text).decode('utf-8')
    except:
        pass
    return text


def separate_words(text):
    def get_replacement(match):
        return f'{match.group(0)[:-1]}. {match.group(0)[-1]}'
    def get_replacement_caps(match):
        return f'{match.group(0)[:-2]}. {match.group(0)[-2:]}'
    text = re.sub(r'[a-z][A-Z]', get_replacement, text)
    text = re.sub(r'[0-9][A-Z]', get_replacement, text)
    text = re.sub(r'[A-Z]{2,}[a-z]', get_replacement_caps, text)
    return text


def preprocess(text):
    text = remove_plain_text_special(text)
    text = remove_links(text)
    text = remove_non_words(text)
    text = remove_whitespace(text)
    text = add_periods(text)
    text = separate_words(text)
    # print(text)
    # print("##########################################")
    return text


if __name__ == '__main__':
    print(preprocess("""ASAPPayment method"""))
