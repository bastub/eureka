import os
import openai
from dotenv import load_dotenv
import PyPDF2 as pdf2
import csv 

load_dotenv()

openai.api_key = os.getenv("gptKey")


def getWord(filename):
    with open (filename, "rb") as f:
        pdf = pdf2.PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        words = text.split()
        f.close()

        liste = []
        # split the words into 500 word chunks
        for i in range(0, len(words), 500):
            liste.append(words[i:i+500])
    return liste

def analyzePDF(filename):
    liste = getWord(filename)
    for i in range(len(liste)):
        convert = " ".join(liste[i])
        p = f'''Donne-moi uniquement les 5 mots les plus représentatifs du texte suivant pour me donner le thème du document:
        {convert}'''

        # generate the response
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=p,
            temperature=.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["12."]
            )

        # grab our text from the repsonse
        text = response['choices'][0]['text']


        print(text+'\n')


# analyzePDF("C:/Users/maxim/Downloads/Listes.pdf")
