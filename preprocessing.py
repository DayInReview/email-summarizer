import re


def remove_non_words(text):
    words = text.split()
    final_words = list()
    for w in words:
        if re.search(r'[^A-Za-z0-9 \,\.\?\:]', w) is None:
            final_words.append(w)
    return ' '.join(final_words)


def add_periods(text):
    text = re.sub(r'\n', '. ', text)
    text = re.sub(r'\ \.', '.', text)
    text = re.sub(r'\.+', '.', text)
    return text


def remove_newlines(text):
    text = re.sub(r'[\r\n]+', '\n', text)
    text = re.sub(r'[\n\r]+', '\n', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n +', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    return text


def remove_links(text):
    text = re.sub(r'http\S+', '', text)
    return text


def remove_plain_text_special(text):
    text = re.sub(r'=0D', '\n', text)
    text = re.sub(r'=0A', '\n', text)
    text = re.sub(r'=\n', '', text)
    return text


def preprocess(text):
    print(text)
    print("#############################################################")
    text = remove_plain_text_special(text)
    text = remove_links(text)
    text = remove_newlines(text)
    text = add_periods(text)
    text = remove_non_words(text)
    print(text)
    print("#############################################################")
    return text


if __name__ == '__main__':
    print(preprocess("""=0D=0AYou have a new response=0D=0A=0D=0Aevent: Controls Weekly M=
eeting F20=0D=0Arespondent: Roie Gal=0D=0A=0D=0AResults so far ..=
.=0D=0A=0D=0Ahttp://whenisgood.net/yy7p7r5/results/h42tmh2=0D=0A=0D=0A=
=0D=0A=0D=0A=0D=0A=0D=0ATo stop getting alerts for just this even=
t, click here ...=0D=0A=0D=0Ahttp://whenisgood.net/NoAlerts?event=
=3Dyy7p7r5=0D=0A=0D=0A=0D=0AWant to know who is sending you these=
 emails? =0D=0AManage what you get here: =0D=0Ahttps://youcanbook=
.me/unsubscribe/?email=3Drishiponnekanti%40gmail.com=0D=0A=0D=0A"""))
