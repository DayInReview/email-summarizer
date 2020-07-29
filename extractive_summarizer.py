from summarizer import Summarizer
import joblib

summary_model = None


def download_model(filename):
    global summary_model
    summary_model = Summarizer()
    joblib.dump(summary_model, filename)


def load_model():
    global summary_model
    filename = 'keras/models/extractive_summarizer.joblib'
    try:
        summary_model = joblib.load(filename)
    except:
        download_model(filename)


def get_summary(text):
    global summary_model
    if summary_model is None:
        return 'ERROR: Model not initialized'
    else:
        return summary_model(text)
