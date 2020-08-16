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
            if re.search(r'[^A-Za-z0-9 \,\.\?\:\n]', w) is None:
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
    try:
        text = quopri.decodestring(text).decode('utf-8')
    except:
        pass
    return text


def preprocess(text):
    text = remove_plain_text_special(text)
    text = remove_links(text)
    text = remove_non_words(text)
    text = remove_whitespace(text)
    text = add_periods(text)
    print(text)
    print("#############################################################")
    return text


if __name__ == '__main__':
    print(preprocess("""How to use React.js to create a Chrome extension in 5 minutes (https://medi=
um.com/@chen/how-to-use-react-js-to-create-chrome-extension-in-5-minutes-2d=
db11899815?source=3Demail-29cc0ffe1e68-1597566465782-digest.reader------1-5=
9------------------9b0aeec2_3b48_43a6_b9aa_df4c30fdd66f-1-34f218f4_d29d_41a=
c_b902_4ac6eb4e9162----&sectionName=3Dtop)"""))
