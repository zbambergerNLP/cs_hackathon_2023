import openai
# Set up your OpenAI API key
openai.organization = "org-JjJq8L2sJ9qYKxxy3JeFSH1u"
openai.api_key = "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"

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

if __name__ == '__main__':
    pass
