import boto3
import boto3.session
import pickle
def dummy_function(access_key,secret_key):
    if access_key!="" and secret_key!="":
        s3client = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        response = s3client.get_object(Bucket='monocalls-models', Key='model_tfidf.pkl')
        body = response['Body'].read()
        model_tfidf = pickle.loads(body)

        response = s3client.get_object(Bucket='monocalls-models', Key='vectorizer_tfidf.pkl')
        body = response['Body'].read()
        vectorizer_tfidf = pickle.loads(body)
        return "Done Successfully With Access Keys"
    else:
        s3client = boto3.client('s3')
        response = s3client.get_object(Bucket='monocalls-models', Key='model_tfidf.pkl')
        body = response['Body'].read()
        model_tfidf = pickle.loads(body)

        response = s3client.get_object(Bucket='monocalls-models', Key='vectorizer_tfidf.pkl')
        body = response['Body'].read()
        vectorizer_tfidf = pickle.loads(body)
        return "Done Successfully Without Access Keys"
