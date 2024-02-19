import CallSummarisation
file_path = ""  # add your own file path of the data
openai_api_key = ""  # add your own API key here
final_data = CallSummarisation.get_call_summarization(file_path, openai_api_key)
print(final_data)
print()
file_path = ""  # add your own file path of the data
final_data = CallSummarisation.get_call_translation(file_path)
print(final_data)
