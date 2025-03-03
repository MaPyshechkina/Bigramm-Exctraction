#Задача: реализовать это правило: 
#поставить все сущ и прил в номинатив кроме > 
#А)слов, которые после предлога. Например, к активам банков — к активам банков 
#Б)слов, которые идут после существительного — активов финансовых организаций — активы финансовых организаций
#проблема: я нашла, как их лемматизировать, это значит, что все трансформруется в Nom, masc, sing, нам нужно сохранить fem и neuter. 

from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


def to_nominative(phrase):
    doc = Doc(phrase)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    words = []
    prev_noun = False  
    prev_prep = False  

    for token in doc.tokens:
        if token.pos == "ADP":  
            words.append(token.text)
            prev_prep = True  
            prev_noun = False  
        elif prev_prep:  
            words.append(token.text)
        elif prev_noun:  
            words.append(token.text)
        else:  # Лемматизируем только само существительное
            token.lemmatize(morph_vocab)
            words.append(token.lemma)
            prev_noun = token.pos == "NOUN"  
            prev_prep = False  

    return " ".join(words)


def load_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        phrases = file.readlines()
    return [phrase.strip() for phrase in phrases]  


file_path = 'corpora_economics/grams.txt'

phrases = load_phrases_from_file(file_path)

corrected_phrases = [to_nominative(phrase) for phrase in phrases]

for original, corrected in zip(phrases, corrected_phrases):
    # print(f"Original: {original}")
    # print(f"Corrected: {corrected}")
    print(corrected)
