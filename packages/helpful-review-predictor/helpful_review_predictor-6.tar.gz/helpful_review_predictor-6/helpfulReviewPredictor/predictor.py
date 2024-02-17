import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import scipy as scipy
import os

class PredictHelpfulness:
    def __init__(self, string):    
        # Load the trained model
        model_file_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
        loaded_model = joblib.load(model_file_path)

        new_text = [string]
        new_overall_rating = [5]

        def preprocess(x):
            x = x.replace(",000,000", " m").replace(",000", " k").replace("′", "'").replace("’", "'")\
                                .replace("won't", " will not").replace("cannot", " can not").replace("can't", " can not")\
                                .replace("n't", " not").replace("what's", " what is").replace("it's", " it is")\
                                .replace("'ve", " have").replace("'m", " am").replace("'re", " are")\
                                .replace("he's", " he is").replace("she's", " she is").replace("'s", " own")\
                                .replace("%", " percent ").replace("₹", " rupee ").replace("$", " dollar ")\
                                .replace("€", " euro ").replace("'ll", " will").replace("how's"," how has").replace("y'all"," you all")\
                                .replace("o'clock"," of the clock").replace("ne'er"," never").replace("let's"," let us")\
                                .replace("finna"," fixing to").replace("gonna"," going to").replace("gimme"," give me").replace("gotta"," got to").replace("'d"," would")\
                                .replace("daresn't"," dare not").replace("dasn't"," dare not").replace("e'er"," ever").replace("everyone's"," everyone is")\
                                .replace("'cause'"," because").replace("i'm"," i am")

            x = re.sub(r"([0-9]+)000000", r"\1m", x)
            x = re.sub(r"([0-9]+)000", r"\1k", x)
            x=re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))',' ',x)
            x=re.sub(r"\\s*\\b(?=\\w*(\\w)\\1{2,})\\w*\\b",' ',x)
            x=re.sub(r'<.*?>',' ',x)
            x=re.sub('[^a-zA-Z]',' ',x)
            x=''.join([i for i in x if not i.isdigit()])
            return x

        new_text_processed = [preprocess(text) for text in new_text]

        # Load the vectorizer
        vectorizer_file_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
        vectorizer = joblib.load(vectorizer_file_path)

        # Transform the input text
        new_text_vectorized = vectorizer.transform(new_text_processed)

        new_overall_rating = np.array(new_overall_rating).reshape(new_text_vectorized.shape[0], 1)
        new_text_vectorized = scipy.sparse.hstack((new_text_vectorized, scipy.sparse.csr_matrix(new_overall_rating)))

        # Make predictions
        predictions = loaded_model.predict(new_text_vectorized)

        # Set result based on predictions
        for i, prediction in enumerate(predictions):
            if prediction == 1:
                self.result = 1
            else:
                self.result = 0
    
    def get_result(self):
        return self.result
