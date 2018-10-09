import json
import nltk
nltk.download("punkt")


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
                sentences = nltk.tokenize.sent_tokenize(msg["Text"])
                for sentence in sentences:
                    if sentence not in ans:
                        ans[sentence] = 1
                    else:
                        ans[sentence] += 1
    return ans