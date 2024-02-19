import boto3.session
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import nltk
nltk.download('punkt')


def get_predictions_of_speaker(dataset,access_key="",secret_key=""):

    # the package is used on sagemaker
    if access_key!="" and secret_key!="":
        s3client = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        response = s3client.get_object(Bucket='monocalls-models', Key='model_tfidf.pkl')
        body = response['Body'].read()
        model_tfidf = pickle.loads(body)

        response = s3client.get_object(Bucket='monocalls-models', Key='vectorizer_tfidf.pkl')
        body = response['Body'].read()
        vectorizer_tfidf = pickle.loads(body)
    else:
        s3client = boto3.client('s3')
        response = s3client.get_object(Bucket='monocalls-models', Key='model_tfidf.pkl')
        body = response['Body'].read()
        model_tfidf = pickle.loads(body)

        response = s3client.get_object(Bucket='monocalls-models', Key='vectorizer_tfidf.pkl')
        body = response['Body'].read()
        vectorizer_tfidf = pickle.loads(body)

    # loading the dataset
    data = pd.read_csv(dataset)

    # cleaning the empty rows from the dataset
    data['utterance'].fillna('', inplace=True)

    # labelling the dataset to numeric form
    label_encoder = LabelEncoder()
    data['Target'] = label_encoder.fit_transform(data['Target'])

    # Preprocessing the data
    indices_to_drop = data[(data['Target'] == 0) & (data['utterance'].apply(lambda x: len(x.split()) < 3))].head(
        600).index
    df = data.drop(indices_to_drop)
    index_drop = df[df['utterance'].apply(lambda x: len(x.split()) < 3)].index
    df1 = df.drop(index_drop)

    # TF-IDF vectorization
    X_test_tfidf = vectorizer_tfidf.transform(df1['utterance'])
    y_pred = model_tfidf.predict(X_test_tfidf)
    df1["predictions"] = y_pred

    return df1[["voice_player_mission_id","utterance","predictions"]]


