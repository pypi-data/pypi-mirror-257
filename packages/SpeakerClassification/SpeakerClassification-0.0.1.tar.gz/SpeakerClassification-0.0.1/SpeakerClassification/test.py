import SpeakerClassification
access_key = ""  # add your own access key here
secret_key = ""  # add your own secret key here
dataset_path = ""  # add your dataset path here
print("Predictions Using the Access Keys")
final_dataframe = (
    SpeakerClassification.get_predictions_of_speaker(dataset_path, access_key, secret_key)
    )
print(final_dataframe.head(5))
