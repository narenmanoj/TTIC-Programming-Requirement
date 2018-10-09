import json
import nltk
nltk.download("punkt")
import pickle


def read_input(filename):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    return data


def get_customer_service_phrases(data):
    ans = {}
    data = data["Issues"]
    for issue in data:
        msg_list = issue["Messages"]
        for msg in msg_list:
            if not msg["IsFromCustomer"]:
                sentences = [s.lower()
                             for s in nltk.tokenize.sent_tokenize(msg["Text"])]
                for sentence in sentences:
                    if sentence not in ans:
                        ans[sentence] = 1
                    else:
                        ans[sentence] += 1
    return ans


def save_object(obj, filename):
    # obtained from https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
    with open(filename, "wb") as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, "rb") as infile:
        return pickle.load(infile)