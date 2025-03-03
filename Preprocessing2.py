#Задача: удалить лишние союзы, местоимения, прилагательные, предлоги
#Проблема: не видит союзы, наверное, нужно список создавать 

from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

# Функция для удаления лишних слов 
def remove_extra_words(phrase):
    doc = Doc(phrase)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    tokens = doc.tokens
    if not tokens:
        return phrase

    # Убираем союз в конце фразы
    if tokens[-1].pos == "CONJ":
        tokens = tokens[:-1] 

    # Убираем союз в начале фразы
    if tokens[0].pos == "CONJ":
        tokens = tokens[1:]  

    # Убираем местоимение в конце фразы
    if tokens and tokens[-1].pos == "PRON":
        tokens = tokens[:-1]  # Убираем последнее местоимение

    # Убираем прилагательное в конце фразы
    if tokens and tokens[-1].pos == "ADJ":
        tokens = tokens[:-1]  

    # Убираем предлог в конце фразы
    if tokens and tokens[-1].pos == "ADP":
        tokens = tokens[:-1]  
    return " ".join([token.text for token in tokens])

def load_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        phrases = file.readlines()
    return [phrase.strip() for phrase in phrases] 


file_path = 'corpora_economics/grams_lem.txt'

phrases = load_phrases_from_file(file_path)

filtered_phrases = [remove_extra_words(phrase) for phrase in phrases]

for original, filtered in zip(phrases, filtered_phrases):
    # print(f"Original: {original}")
    print(filtered)
    # print()
