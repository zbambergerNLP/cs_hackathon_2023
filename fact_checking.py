import openai
# Set up your OpenAI API key
openai.organization = "org-gNs8dlZZWIX5CKD8WDYzaipx"
openai.api_key = "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"
import openai
from numpy import dot
from numpy.linalg import norm
import numpy as np


def get_embadding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def cos_similarty(a, b):
  return dot(a, b)/(norm(a)*norm(b))


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


if __name__ == '__main__':
    evidences = []
    # Insulin support
    text = "The year 2021 marks the 100th anniversary of the discovery of insulin, which has greatly changed the lives of people with diabetes and become a cornerstone of advances in medical science. A rapid bench-to-bedside application of the lifesaving pancreatic extract and its immediate commercialization was the result of a promising idea, positive drive, perseverance, and collaboration of Banting and colleagues. As one of the very few proteins isolated in a pure form at that time, insulin also played a key role in the development of important methodologies and in the beginning of various fields of modern science. Since its discovery, insulin has evolved continuously to optimize the care of people with diabetes. Since the 1980s, recombinant DNA technology has been employed to engineer insulin analogs by modifying their amino acid sequence, which has resulted in the production of insulins with various profiles that are currently used. However, unmet needs in insulin treatment still exist, and several forms of future insulins are under development. In this review, we discuss the past, present, and future of insulin, including a history of ceaseless innovations and collective intelligence. We believe that this story will be a solid foundation and an unerring guide for the future."
    evidences.append(text)
    # dietry support
    text = "Diabetes mellitus (DM) is one of the chronic diseases with higher prevalence worldwide, mainly due to the increase of \"type 2 diabetes\". This increasing is mainly due to the aging of the population, the current epidemic of obesity and the changes in lifestyle, such as high-calorie diets and sedentary lifestyle. In addition, it is common to find that diabetes is associated with obesity, diabesity, or hypertension and hypercholesterolemia, forming part of the socalled Metabolic Syndrome (MS), which is associated with a high probability of developing cardiovascular problems. Despite the advances in the treatment of diabetes, achieving adequate glycemic control in people with diabetes remains difficult, and not always risk free. The diet is one of the bases of the treatment and prevention of diabetes and obesity. This should provide the necessary nutrients for the organism, but also, in the case of diabetic patients, should be coordinated with hypoglycaemic treatment and insulin, called \"nutritional medical treatment\", and whose main objective is normoglycemia. Dietary treatment of obesity is difficult, usually tends to restrict the calories consumed and forgets the psychological factors and lifestyle of patients. However, there is no a unique diet for these pathologies, but it must be individualized, based on the therapeutic objectives adapted to dietary recommendations for the patient's lifestyle."
    evidences.append(text)
    # exercise support
    text = 'Exercise is typically one of the first management strategies advised for patients newly diagnosed with type 2 diabetes. Together with diet and behavior modification, exercise is an essential component of all diabetes and obesity prevention and lifestyle intervention programs. Exercise training, whether aerobic or resistance training or a combination, facilitates improved glucose regulation. High-intensity interval training is also effective and has the added benefit of being very time-efficient. While the efficacy, scalability, and affordability of exercise for the prevention and management of type 2 diabetes are well established, sustainability of exercise recommendations for patients remains elusive.'
    evidences.append(text)
    # alternative support
    text = 'Complementary and alternative medicine (CAM) describes a diverse group of medical and health care systems, practices, and products not currently considered to be part of conventional medicine. Inadequacies in current treatments for diabetes have led 2 to 3.6 million Americans to use CAM for diabetes treatment, despite limited studies of safety and efficacy of CAM methods. CAM is used mostly by West Indians, Africans, Indians, Latin Americans, or Asians. Prayer, acupuncture, massage, hot tub therapy, biofeedback, and yoga have been used as well as various plant remedies for treating diabetes. Several CAM practices and herbal remedies are promising for diabetes treatment, but further rigorous study is needed in order to establish safety, efficacy, and mechanism of action. In the meantime, it is important to be aware that many patients with diabetes may be using CAM and to consider potential interactions with conventional medicines being used.'
    evidences.append(text)
    map = ['Insulin', 'Dietary', 'Exercise', 'Alternative']


    text = "I want to know about treatments for diabeters"
    target = get_embadding(text)
    texts = ["When my child was diagnosed with diabetes, it was a difficult and emotional experience. It was tough to come to terms with the fact that our lives were going to change dramatically, but we were determined to do everything we could to manage the condition and help our child lead a healthy and happy life. We tried a number of different treatments, including insulin therapy and dietary changes. It was a learning curve, and there were some ups and downs along the way, but we persevered and gradually found the right combination of treatments and lifestyle changes that worked for our child. It was a relief to see our child's condition improve over time, and we became much more confident and optimistic about the future. We learned to be proactive about managing diabetes and became more comfortable with things like administering insulin injections and monitoring blood sugar levels. Today, our child is doing much better and living a full and active life. While there are still challenges that come with managing diabetes, we feel much more equipped to handle them and are grateful for the medical advances and resources that have made it possible for our child to thrive.",
             "When my child was first diagnosed with diabetes, I felt overwhelmed and unsure of what to do. We immediately started working with a doctor and a diabetes educator to learn about different treatment options. One of the first treatments we tried was insulin injections. This worked well for my child, and it helped to regulate their blood sugar levels. We also tried an insulin pump, which allowed my child to have more flexibility with their diet and activities. However, we had to make sure to monitor my child's blood sugar levels closely to avoid complications. We also made changes to our child's diet, focusing on healthy, whole foods and limiting sugar and carbohydrates. We found that this helped to control their blood sugar levels and improve their overall health. We worked with a registered dietitian to create a meal plan that worked for our family. Another treatment we tried was regular exercise. We found that exercise helped to lower my child's blood sugar levels and improve their overall health. We made sure to talk to our doctor about safe exercise options and how to adjust my child's insulin dosage to compensate for the activity. We also tried some alternative treatments, such as herbal remedies and acupuncture. While we found that these treatments had some benefits, they were not as effective as the traditional treatments we were using. Overall, we learned that managing diabetes requires a combination of different treatments and a willingness to adapt and make changes as needed. While there were some treatments that didn't work as well as others, we were able to find a combination that worked for our child and helped them to live a happy, healthy life.",
             "It's been a few months since my child was diagnosed with diabetes, and it's been a rollercoaster ride of emotions and treatments. At first, we were in shock and didn't know what to do. We talked to a few doctors, but it was overwhelming to try to make sense of all the medical jargon and treatment options. We started with some medication to help manage their blood sugar levels, but it wasn't enough. We had to completely overhaul our diet and lifestyle. We cut out all processed foods, sugary drinks, and carbs. We started exercising more and monitoring our blood sugar levels regularly. It was a big adjustment for all of us, but we knew it was necessary for our child's health. We also talked to several specialists who helped us with different aspects of diabetes management. We saw an endocrinologist, Dr. Art Vandelay who helped us fine-tune our medication dosage and taught us how to use an insulin pump. We saw a dietitian, Lena Collins, who gave us practical tips on how to prepare healthy meals and snacks. And we saw a therapist, Girishwar Undurti, who helped us cope with the stress and anxiety that came with the diagnosis. It hasn't been easy, and there have been ups and downs, but I'm grateful for the progress we've made. We're learning to live with diabetes, rather than letting it control our lives. We're taking it one day at a time and trying our best to stay positive and hopeful for the future.",
             "I remember the day when the doctor told us our child had cancer. It was like the world stopped spinning. We were devastated. We talked to several doctors and tried different treatments. We started with chemotherapy, which made our child very sick, but we had to keep going. We also tried radiation therapy, but the side effects were unbearable. It was tough seeing our child in so much pain. We consulted with Dr. Smith, a renowned oncologist, who recommended a targeted therapy that was still in the experimental phase. We were hesitant at first, but desperate times call for desperate measures. We took a chance and tried it, and it worked! Our child's cancer went into remission. We also talked to Dr. Rodriguez, a pediatrician who was very supportive throughout the entire process. She helped us understand the treatment options and guided us in making the best decisions for our child's health. It was a rollercoaster of emotions, but we never gave up hope. We were lucky to have a supportive medical team and a community of friends and family who were there for us every step of the way.",
             "My child was diagnosed with Pancreatitis last year, and it was one of the scariest moments of my life. We tried a few different treatments, but it was a long and difficult journey to find the right one. At first, we tried pain management medication and dietary changes, but those weren't effective enough. We ended up seeing a gastroenterologist, Dr. Smith, who recommended enzyme replacement therapy to help with digestion. That was a game-changer for my child's comfort and well-being. We also saw a nutritionist to help us with meal planning and managing my child's dietary needs. It was a challenging time, but we were lucky to have such caring and knowledgeable doctors on our side. We still have to be vigilant and keep a close eye on my child's health, but we're managing the disease as best we can."]
    
    cos = [cos_similarty(get_embadding(x), target) for x in texts]
    cos = np.array(cos)
    threshold = 0.8
    # find indices of top 3 cos elements that are above threshold
    top3 = cos.argsort()[-3:][::-1]
    indices = cos > threshold
    indices = [i for i in top3 if indices[i]]
    # print(indices)
    texts = [texts[i] for i in indices]

    for text in texts:
        prompt_to_check = text_analyzer(text)
        classifications = classify_claims(prompt_to_check, evidences)

        # for i, prompt in enumerate(prompt_to_check):
        #     prompt = prompt.split(' is a treatment for ')[0]
        #     print('Treatment: ', prompt)
        #     for j, c in enumerate(classifications[i]):
        #         if c:
        #             print(f'True for article on: {map[j]}')
        #     print('')



    text = "My child has diabetes, which dietitian can help me"
    cos = [cos_similarty(get_embadding(x), target) for x in texts]
    cos = np.array(cos)
    threshold = 0.8
    # find indices of top 3 cos elements that are above threshold
    top3 = cos.argsort()[-3:][::-1]
    indices = cos > threshold
    indices = [i for i in top3 if indices[i]]
    # print(indices)
    for text in texts:
        prompt_to_check = text_analyzer(text)
        classifications = classify_claims(prompt_to_check, evidences)
