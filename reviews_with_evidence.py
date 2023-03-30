import openai
# Set up your OpenAI API key
openai.organization = "org-gNs8dlZZWIX5CKD8WDYzaipx"
openai.api_key = 
import openai
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util


def sentence_bert_compute_similarity(
        model: SentenceTransformer,
        sentences1: str,
        sentences2: str) -> float:
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)
    return util.cos_sim(embeddings1, embeddings2)


def chat_gpt_claim_check(claim, evidence):
    prompt = f"text: {evidence}" \
             f"claim: {claim}" \
             "is there a support for the claim in the text? return yes or no"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
        ]
    )

    message = response.choices[0].message.content
    return message


def classify_claims(claims, evidences):
    claims_t_f = [[False] * len(evidences) for _ in range(len(claims))]
    for i, claim in enumerate(claims):
        for j, evidence in enumerate(evidences):
            response = chat_gpt_claim_check(claim, evidence)
            if 'Yes' in response or 'yes' in response or 'YES' in response:
                claims_t_f[i][j] = True
    return claims_t_f


def text_analyzer(text):
    prompt = f"{text}\n" \
             "Write in a single word the disease that is described."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
        ]
    )

    disease = response.choices[0].message.content
    if disease.lower().replace('.','') not in text.lower():
        raise ValueError("The disease is not in the text")

    prompt = f"{text}\n" \
             "Write the treatments in this text as a numbered list."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
        ]
    )

    treatments = response.choices[0].message.content
    treatments = treatments.split('\n')
    for i, treatment in enumerate(treatments):
        treatments[i] = treatment.split('.')[1]

    prompts_to_check = [f"{treatment} is a treatment for {disease}" for treatment in treatments]
    return prompts_to_check


def fact_checker(query):
    data = pd.read_excel("data.xlsx")
    evidence = pd.read_excel("evidence.xlsx")
    reviews = data[data.type == 1]['text'].values
    evidences = evidence['text'].values
    links = evidence['links'].values

    sbert_model = SentenceTransformer('sentence-transformers/msmarco-distilbert-base-v4')
    top_reviews = []
    cos = [sentence_bert_compute_similarity(sbert_model, query, x).item() for x in reviews]
    cos = np.array(cos)
    top = cos.argsort()[-2:][::-1]
    texts = [reviews[i] for i in top]

    for text in texts:
        prompt_to_check = text_analyzer(text)
        classifications = classify_claims(prompt_to_check, evidences)
        dict = {'review': text, 'links': []}
        for c1 in classifications:
            for i, c2 in enumerate(c1):
                if c2 and links[i] not in dict['links']:
                    dict['links'].append(links[i])
        top_reviews.append(dict)

    return top_reviews


if __name__ == '__main__':
    fact_checker('My child has diabetes, which dietitian can help me')
