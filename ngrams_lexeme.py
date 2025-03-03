import pandas as pd
import spacy

nlp = spacy.load("ru_core_news_sm")

file_path = "corpora_economics/34gram.csv"
df = pd.read_csv(file_path)

if 'merged' not in df.columns:
    raise ValueError("Колонка 'merged' не найдена в CSV файле.")

corpus = df['merged'].dropna().tolist()

# Заготовочная лексема
lexeme = "актив"

# Функция для получения всех лемм и форм для слова "Х"
def generate_variations(word):
    doc = nlp(word)
    base_form = doc[0].lemma_  # Лемма для слова
    variations = [base_form]  # Начинаем с самой леммы

    # Формируем дополнительные вариации на основе склонений
    for token in doc:
        if token.dep_ == "case" and token.pos_ != "PUNCT":
            variations.append(token.text)  # Добавляем склоненные формы

    return list(set(variations))

# Получение вариаций для слова "Х"
lexeme_variations = generate_variations(lexeme)
print(f"Вариации для слова '{lexeme}': {lexeme_variations}")

# Нахождение всех уникальных н-грамм, содержащих слово "Х" и его вариации
sentences_with_lexeme = [sentence for sentence in corpus if
                         any(variation in sentence for variation in lexeme_variations)]
unique_sentences_with_lexeme = list(set(sentences_with_lexeme))  # Убираем дубли


print(f"\nУникальные н-граммы со словом '{lexeme}':")
for sentence in unique_sentences_with_lexeme:
    print(sentence)
