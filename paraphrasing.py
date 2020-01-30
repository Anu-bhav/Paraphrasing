#!/usr/bin/env python3
"""
Author: Anubhav
Date: 29.01.2020

The program will take a processed textfile as input, the file should have every sentence in a new line

Login Info to get cookies
https://quillbot.com/
Email: prinusam.roy.9e@819760.com
Password: password
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
        "__cfduid": "d90a7ce3fa0772a83274fe34ad8c58a9f1580405470;",
        "_ga": "GA1.2.1926625509.1580405472;",
        "_gid": "GA1.2.1282073988.1580405472;",
        "sessID": "b0f5b816e094bfea;",
        "connect.sid": "s%3AwdYjihyTxyB5J_BoJ3_n1dVy3P5kGPUQ.IYeruJ47DcK7AIqj%2BjbKlkZkOmDeV1BccWwf%2BYTKKk4;",
        "authenticated": "true;",
        "premium": "true;",
        "quid": "RqEHTeLDBPcZTsI1rYo5Mfcu3d02;",
        "__stripe_sid": "28dae5a8-98b1-4420-9ade-fc7fe1be84a1;",
        "__stripe_mid": "3b243369-c00a-49f1-b007-c3d49ad4e2b6;",
        "amplitude_id_6e403e775d1f5921fdc52daf8f866c66quillbot.com": "eyJkZXZpY2VJZCI6IjgzYzAzZTc0LThhMzktNDAwYS1hNDA5LWI4MzZkNDhhM2FiZFIiLCJ1c2VySWQiOiJwcmludXNhbS5yb3kuOWVAODE5NzYwLmNvbSIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU4MDQwNTQ3MzMxNCwibGFzdEV2ZW50VGltZSI6MTU4MDQwNTYyMDEzNSwiZXZlbnRJZCI6MywiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjN9;",
        "_gat": "1;",
        "userIDToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1OTc0MmQyNjlhY2IzNWZiNjU3YzBjNGRkMmM3YjcyYWEzMTRiNTAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGFyYXBocmFzZXItNDcyYzEiLCJhdWQiOiJwYXJhcGhyYXNlci00NzJjMSIsImF1dGhfdGltZSI6MTU4MDQwNTUyMCwidXNlcl9pZCI6IlJxRUhUZUxEQlBjWlRzSTFyWW81TWZjdTNkMDIiLCJzdWIiOiJScUVIVGVMREJQY1pUc0kxcllvNU1mY3UzZDAyIiwiaWF0IjoxNTgwNDA1NjIxLCJleHAiOjE1ODA0MDkyMjEsImVtYWlsIjoicHJpbnVzYW0ucm95LjllQDgxOTc2MC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJwcmludXNhbS5yb3kuOWVAODE5NzYwLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.dhiWkSZFqb6VkyJunASN9sgHdNDe5BffVaB8iX7qw479aB-nzu8L5psbn3ev2nw3r2raYEVD-1jHYXic-GyR_LO6pPWfqbvrcCnkZDkUVLiAIVQjB09CSFh5bqL_L7Zp6imLzgT6Tk6mk162FyZYD9DxLYy7KpsyJEhc41TQX-66hWkce2Zghl0VTjWUcF-Jszo66nAC1aAUHMDOA8umMAewlVVKf05MlRKY-Gs9xuMWenr3-gUV4pgCUk5acApqe84K7uJPIXEbmYH_35o7X0f1hxB8KbcbRUTEFwA-Clu8SnZu3dbblGf7YbNHeWmZYeLB7jGHugDQp5GlAFYojg"
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
