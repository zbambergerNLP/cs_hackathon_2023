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
    deberta_model = DebertaV2Model.from_pretrained("microsoft/deberta-v2-xlarge")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v2-xlarge")
    sentence_1 = "the sky is blue"
    sentence_2 = "the sky is gray"
    sentence_3 = 'I farted'
    deberta_similarity_1_2 = deberta_compute_similarity(deberta_model, tokenizer, sentence_1, sentence_2)
    print(f'the similarity between sentences 1 and 2 according to deberta is: {deberta_similarity_1_2}')
    deberta_similarity_1_3 = deberta_compute_similarity(deberta_model, tokenizer, sentence_1, sentence_3)
    print(f'the similarity between sentences 1 and 3 according to deberta is {deberta_similarity_1_3}')

    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    sbert_similarity_1_2 = sentence_bert_compute_similarity(sbert_model, sentence_1, sentence_2)
    sbert_similarity_1_3 = sentence_bert_compute_similarity(sbert_model, sentence_1, sentence_3)
    print(f'the similarity between sentences 1 and 2 according to sbert is: {sbert_similarity_1_2}')
    print(f'the similarity between sentences 1 and 3 according to sbert is {sbert_similarity_1_3}')

