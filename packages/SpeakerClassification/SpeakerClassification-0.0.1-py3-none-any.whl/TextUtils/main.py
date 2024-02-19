
def get_utterances(raw_data_dict):
    if type(raw_data_dict) == str:
        raw_data_dict = eval(raw_data_dict)

    try:

        channels = [c['channel'] for c in raw_data_dict["results"]["utterances"]]
        transcript = [c['transcript'] for c in raw_data_dict["results"]["utterances"]]
        confidence = [c['confidence'] for c in raw_data_dict["results"]["utterances"]]

        return channels, transcript, confidence

    except Exception as e:
        return str(e)


def get_transcripts(raw_data_dict):
    if type(raw_data_dict) == str:
        raw_data_dict = eval(raw_data_dict)

    try:
        if raw_data_dict.get("results",None) != None:
            if len(raw_data_dict.get("results").get("channels")) == 2:

                se_transcript = raw_data_dict["results"]["channels"][0]["alternatives"][0]["transcript"]
                lead_transcript = raw_data_dict["results"]["channels"][1]["alternatives"][0]["transcript"]

                return se_transcript, lead_transcript

            else:
                return "Mono call"
        else:
            return "Deepgram output doesn't satisfy pipeline requirements"

    except Exception as e:
        return str(e)


def convert_to_script(channels, transcript):
    new_ch, new_tx = [], []

    i = 0
    stack = []

    channels.append(-1)

    while i <= len(channels) - 2:
        stack.append(transcript[i])

        if channels[i] != channels[i + 1]:
            new_tx.append(" ".join(stack))
            new_ch.append(channels[i])
            stack = []

        i += 1

    return new_ch, new_tx