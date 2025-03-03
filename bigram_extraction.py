from yandex_cloud_ml_sdk import YCloudML
import pandas as pd


def extract_bigrams(input_file, output_file, folder_id, auth):
    with open(input_file, "r", encoding="utf-8") as file:
        trigrams = [line.strip() for line in file if line.strip()]

    sdk = YCloudML(folder_id=folder_id, auth=auth)
    results = []

    for trigram in trigrams:
        messages = [
            {"role": "system",
             "text": "Ты — AI, который извлекает биграммы из н-грамм. Н-грамма – это фраза из трех и более слов. Биграмма – это осмысленная фраза из двух слов."},
            {"role": "user", "text": f"Найди биграмму в триграмме: {trigram}"},
        ]

        try:
            result = sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)
            bigram = result[0].text.strip() if result else "Ошибка"
        except Exception as e:
            print(f"Ошибка обработки триграммы: {trigram}\n{e}")
            bigram = "Ошибка"

        results.append({"Trigram": trigram, "Bigram": bigram})

    pd.DataFrame(results).to_csv(output_file, index=False, encoding="utf-8")
    print(f"Результаты сохранены в файл: {output_file}")


if __name__ == "__main__":
    folder_id, auth = "ваш folder-id", "ваш API KEY"
    extract_bigrams("corpora_economics/grams_lem.txt", "extracted_bigramssss.csv", folder_id, auth)
