import transformers
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, DebertaV2Model, PreTrainedTokenizer
import torch


def sentence_bert_compute_similarity(
        model: SentenceTransformer,
        sentences1: str,
        sentences2: str) -> float:
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)
    return util.cos_sim(embeddings1, embeddings2)


def deberta_compute_similarity(
        model: DebertaV2Model,
        tokenizer: transformers.PreTrainedTokenizer,
        sentences1: str,
        sentences2: str) -> float:
    tokenized_sentences1 = tokenizer(sentences1)
    tokenized_sentences2 = tokenizer(sentences2)
    embeddings1 = model(**tokenized_sentences1).last_hidden_state[:, 0, :]
    embeddings2 = model(**tokenized_sentences2).last_hidden_state[:, 0, :]
    return util.cos_sim(embeddings1, embeddings2)


if __name__ == '__main__':
    deberta_model = DebertaV2Model.from_pretrained("microsoft/deberta-v2")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v2")
    sentence_1 = "the sky is blue"
    sentence_2 = "the sky is gray"
    sentence_3 = 'I farted'

    text = "I want to know about treatments for diabeters"
    texts = [
        "When my child was diagnosed with diabetes, it was a difficult and emotional experience. It was tough to come to terms with the fact that our lives were going to change dramatically, but we were determined to do everything we could to manage the condition and help our child lead a healthy and happy life. We tried a number of different treatments, including insulin therapy and dietary changes. It was a learning curve, and there were some ups and downs along the way, but we persevered and gradually found the right combination of treatments and lifestyle changes that worked for our child. It was a relief to see our child's condition improve over time, and we became much more confident and optimistic about the future. We learned to be proactive about managing diabetes and became more comfortable with things like administering insulin injections and monitoring blood sugar levels. Today, our child is doing much better and living a full and active life. While there are still challenges that come with managing diabetes, we feel much more equipped to handle them and are grateful for the medical advances and resources that have made it possible for our child to thrive.",
        "When my child was first diagnosed with diabetes, I felt overwhelmed and unsure of what to do. We immediately started working with a doctor and a diabetes educator to learn about different treatment options. One of the first treatments we tried was insulin injections. This worked well for my child, and it helped to regulate their blood sugar levels. We also tried an insulin pump, which allowed my child to have more flexibility with their diet and activities. However, we had to make sure to monitor my child's blood sugar levels closely to avoid complications. We also made changes to our child's diet, focusing on healthy, whole foods and limiting sugar and carbohydrates. We found that this helped to control their blood sugar levels and improve their overall health. We worked with a registered dietitian to create a meal plan that worked for our family. Another treatment we tried was regular exercise. We found that exercise helped to lower my child's blood sugar levels and improve their overall health. We made sure to talk to our doctor about safe exercise options and how to adjust my child's insulin dosage to compensate for the activity. We also tried some alternative treatments, such as herbal remedies and acupuncture. While we found that these treatments had some benefits, they were not as effective as the traditional treatments we were using. Overall, we learned that managing diabetes requires a combination of different treatments and a willingness to adapt and make changes as needed. While there were some treatments that didn't work as well as others, we were able to find a combination that worked for our child and helped them to live a happy, healthy life.",
        "It's been a few months since my child was diagnosed with diabetes, and it's been a rollercoaster ride of emotions and treatments. At first, we were in shock and didn't know what to do. We talked to a few doctors, but it was overwhelming to try to make sense of all the medical jargon and treatment options. We started with some medication to help manage their blood sugar levels, but it wasn't enough. We had to completely overhaul our diet and lifestyle. We cut out all processed foods, sugary drinks, and carbs. We started exercising more and monitoring our blood sugar levels regularly. It was a big adjustment for all of us, but we knew it was necessary for our child's health. We also talked to several specialists who helped us with different aspects of diabetes management. We saw an endocrinologist, Dr. Art Vandelay who helped us fine-tune our medication dosage and taught us how to use an insulin pump. We saw a dietitian, Lena Collins, who gave us practical tips on how to prepare healthy meals and snacks. And we saw a therapist, Girishwar Undurti, who helped us cope with the stress and anxiety that came with the diagnosis. It hasn't been easy, and there have been ups and downs, but I'm grateful for the progress we've made. We're learning to live with diabetes, rather than letting it control our lives. We're taking it one day at a time and trying our best to stay positive and hopeful for the future.",
        "I remember the day when the doctor told us our child had cancer. It was like the world stopped spinning. We were devastated. We talked to several doctors and tried different treatments. We started with chemotherapy, which made our child very sick, but we had to keep going. We also tried radiation therapy, but the side effects were unbearable. It was tough seeing our child in so much pain. We consulted with Dr. Smith, a renowned oncologist, who recommended a targeted therapy that was still in the experimental phase. We were hesitant at first, but desperate times call for desperate measures. We took a chance and tried it, and it worked! Our child's cancer went into remission. We also talked to Dr. Rodriguez, a pediatrician who was very supportive throughout the entire process. She helped us understand the treatment options and guided us in making the best decisions for our child's health. It was a rollercoaster of emotions, but we never gave up hope. We were lucky to have a supportive medical team and a community of friends and family who were there for us every step of the way.",
        "My child was diagnosed with Pancreatitis last year, and it was one of the scariest moments of my life. We tried a few different treatments, but it was a long and difficult journey to find the right one. At first, we tried pain management medication and dietary changes, but those weren't effective enough. We ended up seeing a gastroenterologist, Dr. Smith, who recommended enzyme replacement therapy to help with digestion. That was a game-changer for my child's comfort and well-being. We also saw a nutritionist to help us with meal planning and managing my child's dietary needs. It was a challenging time, but we were lucky to have such caring and knowledgeable doctors on our side. We still have to be vigilant and keep a close eye on my child's health, but we're managing the disease as best we can."]
    cos = [deberta_compute_similarity(deberta_model, tokenizer, text, x) for x in texts]

    deberta_similarity_1_2 = deberta_compute_similarity(deberta_model, tokenizer, sentence_1, sentence_2)
    print(f'the similarity between sentences 1 and 2 according to deberta is: {deberta_similarity_1_2}')
    deberta_similarity_1_3 = deberta_compute_similarity(deberta_model, tokenizer, sentence_1, sentence_3)
    print(f'the similarity between sentences 1 and 3 according to deberta is {deberta_similarity_1_3}')

    # sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    # sbert_similarity_1_2 = sentence_bert_compute_similarity(sbert_model, sentence_1, sentence_2)
    # sbert_similarity_1_3 = sentence_bert_compute_similarity(sbert_model, sentence_1, sentence_3)
    # print(f'the similarity between sentences 1 and 2 according to sbert is: {sbert_similarity_1_2}')
    # print(f'the similarity between sentences 1 and 3 according to sbert is {sbert_similarity_1_3}')

