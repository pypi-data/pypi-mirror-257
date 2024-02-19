import boto3
import pandas as pd
import os
import json
import botocore
from tqdm import tqdm
import logging
tqdm.pandas()

def fetch_audio_file_from_s3_bucket(bucket_name):
    # Initialize an S3 client
    s3 = boto3.client('s3')
    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='folder-name')
    local_directory = 'audio_data'

    # Iterate through the objects in the bucket
    for obj in response.get('Contents', []):
        # Extract the key (object key)
        object_key = obj['Key']
        try:
            # Download the WAV file
            wav_data = s3.get_object(Bucket=bucket_name, Key=object_key)
            # Save the WAV data to a local file
            local_file_path = os.path.join(local_directory, os.path.basename(object_key))
            with open(local_file_path, 'wb') as local_file:
                local_file.write(wav_data['Body'].read())
            print(f"Downloaded {object_key} to {local_file_path}")
        except Exception as e:
            print(f"Failed to fetch WAV: {object_key} - {str(e)}")


def fetch_files_from_s3_bucket(bucket_name):
    # Initialize an S3 client
    s3 = boto3.client('s3')
    # Replace with your S3 bucket name
    bucket_name = 'transcription-pipeline-prod'
    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='input/20231004')
    # Iterate through the objects in the bucket
    for obj in response.get('Contents', []):
        # Extract the key (object key) and the folder name
        object_key = obj['Key']
        try:
            csv_data = s3.get_object(Bucket=bucket_name, Key=object_key)
            df_temp = pd.read_csv(csv_data['Body'])
            df_temp.to_csv('data/{}.csv'.format(object_key.split("/")[-2]))
        except:
            print("failed to fetch csv: ", object_key.split("/")[-2])


def access_transcript_s3():
    txr_urls = pd.DataFrame()

    def get_transcription_data(asr_uuid):
        s3 = boto3.resource("s3")
        key = "{0}.json".format(asr_uuid)
        bucket_name = "squad-transcription-data"
        obj = s3.Bucket(bucket_name).Object(key)

        try:
            response = obj.get()
        except botocore.exceptions.ClientError as error:
            logging.logger.info("Error in fetching transcription from s3 bucket for asr_uuid : {0}".format(asr_uuid))
            return error.response["ResponseMetadata"]["HTTPStatusCode"], None

        data = response["Body"].read().decode("utf-8")
        resp_data = json.loads(data)

        return resp_data

    # txr_urls is the dataframe which contains raw_data_s3_url
    # from the table voice_integrations_vpmtranscriptdataasr
    txr_urls["raw_data"] = txr_urls["raw_data_s3_url"].progress_apply(
        lambda x: get_transcription_data(x.split("/")[-1].split(".")[0]))
    
    return txr_urls