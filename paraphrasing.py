#!/usr/bin/env python3
"""
Author: Anubhav
Date: 29.01.2020

The program will take a processed textfile as input, the file should have every sentence in a new line
"""
import os.path
from json import loads
from urllib.parse import quote
from docx import Document
import requests

API_URL = "https://quillbot.com/api/singleParaphrase"
PARAMS = "?userID=N/A&text={}&strength={}&autoflip={}&wikify={}&fthresh={}"
DOC = Document()


def setup_session():
    """Update headers for the session.

    Returns
    -------
    obj
        Requests Session
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Content-Type": "application/text"
        }
    )
    return session


def get_parameterized_url(text):
    """Gets parametrized url

    Parameters
    ----------
    text : str

    Returns
    -------
    url: str
        string containing url and quoted text
    """
    url_encoded_text = quote(text)
    autoflip = "true"
    fthresh = "true"
    strength = "4"
    wikify = "9"
    url = API_URL + PARAMS.format(url_encoded_text, strength, autoflip, wikify, fthresh)
    return url


def openfile(filepath):
    """open the txt file to be process and saves it to a docx file

    Arguments:
        filepath {string} -- the path, that the user inputs
    """

    filepath = filepath.rstrip()
    filesave = os.path.split(filepath)[-1]
    filesave = ([filename.strip() for filename in filesave.split('.')][-2] + " - draft")

    cur_path = os.path.dirname(__file__)
    textfile = os.path.relpath(filepath, cur_path)

    with open(textfile, "r") as wholetext:
        for line in wholetext:
            line = line.rstrip()

            session = setup_session()
            if len(line) > 700:
                print("line should be less than 700 characters, %s" % line)
            else:
                url = get_parameterized_url(line)
                paraphrasor(url, session)
                DOC.save('%s.docx' % filesave)
    wholetext.close()


def paraphrasor(url, session):
    """Gets paraphrased text

    Parameters
    ----------
    url : str
        Complete url containing text
    session : class `requests.sessions.Session`
            Requests session.
            Provides cookie persistence, connection-pooling, and configuration.
    """
    # Cookies are configurable
    cookies = {
        "__cfduid": "deaff692a20199c189d2fc18b1e1b81ce1578851672;",
        "_ga": "GA1.2.1058973520.1578851672;",
        "amplitude_id_6e403e775d1f5921fdc52daf8f866c66quillbot.com": "eyJkZXZpY2VJZCI6ImM5YmM2NDk2LWFiMDAtNDJmNC1hNDY1LTljMjNmNTUxZWI2NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU3ODg1MTY3MjgwOSwibGFzdEV2ZW50VGltZSI6MTU3ODg1MTY3MjgwOSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9;",
        "sessID": "c1d8a534715fec4e;",
        "_gid": "GA1.2.1411973136.1580293871;",
        "premium": "true;",
        "userIDToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1OTc0MmQyNjlhY2IzNWZiNjU3YzBjNGRkMmM3YjcyYWEzMTRiNTAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGFyYXBocmFzZXItNDcyYzEiLCJhdWQiOiJwYXJhcGhyYXNlci00NzJjMSIsImF1dGhfdGltZSI6MTU4MDI5NTk4MSwidXNlcl9pZCI6InRVeUZJRUZXd2dXSjl2RUszNzlXUEdSRnBxeTEiLCJzdWIiOiJ0VXlGSUVGV3dnV0o5dkVLMzc5V1BHUkZwcXkxIiwiaWF0IjoxNTgwMjk1OTgyLCJleHAiOjE1ODAyOTk1ODIsImVtYWlsIjoiMWVyLm1la25lczIwMTRAY3lmdS5pY3UiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyIxZXIubWVrbmVzMjAxNEBjeWZ1LmljdSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.lWr63CbAj168AbAFoDjlR5V-ulN187_hbtHYqOcf461_dVOqa6zuhhoSn1LjrZ6O7aqIJC1lgNN0-1pXl_rGDZXSkG_YXoxkAlKdC1KzM-Gck2djEQ6Zj7VCbsimdVMZWPAVjGq6OYrbm9i9FixXmMz4gs2yYIkeulfm-y8zlt-oWpGKf2nrEEdk7WMeLOlQc6vHrerTeO0weuNydsWWw4ndoGmfFrimRc5ehc2nONC7--AhAHgeggnEfdbwM9k8UjVU0UJilNVn5A87OdLJ7GFepvE4u0xVOQjoeFGOO0y7ZrqRLATOqxbuKt0XvquyLcu8uYlfgrx73ZtlX13fvw;",
        "connect.sid": "s%3AUWl0su0IriH7t-5FtJMaanB0OnbrycOY.QHFucYo4RdOeHKk5EjkaWiZamDuFIOcD3AozTTOtHCo;",
        "authenticated": "true;",
        "quid": "tUyFIEFWwgWJ9vEK379WPGRFpqy1"
    }

    req = session.get(url, cookies=cookies)
    if req.status_code == 200:
        json_text = loads(req.text)

        end = "\n\n"

        json_text = json_text[0] if len(json_text) == 1 else json_text
        print(f"\nData Sent: {json_text['sent']}", end)
        DOC.add_paragraph(f"\nData Sent: {json_text['sent']}")

        paras = [key for key in json_text if key.startswith("paras")]
        texts = list(
            {text.get("alt") for para in paras for text in json_text[para]}
        )

        print("Alternative Texts:")
        DOC.add_paragraph("Alternative Texts:")

        print("_" * 90, "\n")
        DOC.add_paragraph("_" * 90)
        DOC.add_paragraph()

        for text in texts:
            print(text, end)
            DOC.add_paragraph(text)

        print("#" * 90)
        DOC.add_paragraph("#" * 90)


def main():
    """main function the program starts
    """
    print("Quillbot Paraphrasing tool.")
    filepath = input("Enter the path of the formated text file: ")
    openfile(filepath)


if __name__ == "__main__":
    main()
