import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import tiktoken
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from nltk.tokenize import word_tokenize
import string
import re
from deep_translator import GoogleTranslator
from tqdm import tqdm


def get_call_summarization(file_path, openai_api_key):

    df = pd.read_csv(file_path)
    df['transcription'] = df['se_translated_transcript'] + " " + df['lead_translated_transcript']
    df = df[df['transcription'].notnull()]
    model_name = "gpt-3.5-turbo"
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=model_name)
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)

    prompt_template = """Write a concise summary of the following:


    {text}


    CONSCISE SUMMARY IN ENGLISH:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    stop_words = ['hello', 'sir', 'maam', 'good', 'afternoon', 'morning', 'evening', 'name',
                  'calling', 'talking', 'speaking', 'behalf', 'yes', 'no', 'ok', 'okay', 'right', 'ji',
                  'okay', 'thank', 'sure', 'also', 'tell', 'want']

    def preprocess_text(text):
        text = text.lower()
        text = text.strip()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        text = text.replace(' cx ', ' customer ').replace('se', ' sales executive ')
        tokens = word_tokenize(text)
        filtered_text = [word for word in tokens if (word not in stop_words) and len(word) > 2]
        text = ' '.join(filtered_text)
        return text

    chain1 = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=True)
    chain2 = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt,
                                  verbose=True)

    for index, row in df.iterrows():
        try:
            transcript = row['transcription']
            texts = text_splitter.split_text(transcript)
            docs = [Document(page_content=t) for t in texts]
            verbose = True
            summary = chain1.run(docs)
            df.at[index, 'ACPT Remarks'] = summary

        except Exception as e:
            df.at[index, "se_translated_transcript"] = preprocess_text(df.at[index, "se_translated_transcript"])
            df.at[index, "lead_translated_transcript"] = preprocess_text(df.at[index, "lead_translated_transcript"])
            transcript = row['se_translated_transcript']
            texts = text_splitter.split_text(transcript)
            docs = [Document(page_content=t) for t in texts]
            verbose = True
            summary = chain1.run(docs)
            df.at[index, 'ACPT Remarks'] = summary

            transcript = row['lead_translated_transcript']
            texts = text_splitter.split_text(transcript)
            docs = [Document(page_content=t) for t in texts]
            verbose = True
            summary = chain1.run(docs)
            df.at[index, 'ACPT Remarks'] += summary

    df = df[df['ACPT Remarks'].notnull()]

    return df


def get_call_translation(filepath):
    df_pandas = pd.read_csv(filepath)

    def translate_large_text(text, translator_object):

        parts = 1
        success = False
        words = text.split(" ")

        while not success:
            translation = ""
            try:

                for i in range(0, parts):
                    section = " ".join(words[i * (len(words) // parts):(i + 1) * (len(words) // parts)])
                    translated_section = translator_object.translate(text=section)
                    translation += translated_section + " "
                success = True
            except Exception as e:
                parts *= 2

        return translation

    df_pandas['se_translated_transcript'] = ""
    df_pandas['lead_translated_transcript'] = ""

    g_translator = GoogleTranslator(source='hindi', target='en')

    for i in tqdm(range(df_pandas.shape[0])):
        try:
            df_pandas['se_translated_transcript'][i] = translate_large_text(
                eval(df_pandas['responses'][i])['results'][0]['transcription']['0'], g_translator)
        except:
            df_pandas['se_translated_transcript'][i] = ""
        try:
            df_pandas['lead_translated_transcript'][i] = translate_large_text(
                eval(df_pandas['responses'][i])['results'][0]['transcription']['1'], g_translator)
        except:
            df_pandas['lead_translated_transcript'][i] = ""

    return df_pandas









