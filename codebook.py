from collections import Counter
import re

#Преобразует txt файл в строку
def read_text(path: str = "examples/input.txt") -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


#Убирает пробелы ентер переносы
def clean(txt: str) -> list:
    content = re.sub(r"[^\w\s]", "", txt)
    return content.split()

#Считает все символы в строке
def count(txt: str) -> list:
    counter = Counter(txt)
    return [char for char, _ in counter.most_common()]

#Добавляет в answer все подстроки слова slovo и увеличивает их счётчики
def razbr(slovo: str, answer: dict) -> dict:
    c = 0
    bat = len(slovo)
    i = 1
    while bat > 0:
        mix = len(slovo[:i])
        string = slovo[:i]
        while mix > 0:
            mix -= 1
            c += 1
            if string in answer:
                answer[string] += 1
            else:
                answer[string] = 1
            string = string[1:]
        bat -= 1
        i += 1
    return answer

#Добавляет кодировку для всего словаря
def build(answer):
    counter = 0
    for key in answer:
        answer[key] = [answer[key], str(counter)]
        counter += 1
    return answer

#Удаляет подстроки, чей код 'длиннее' конкатенации кодов её символов
def check(answer):
    for key in list(answer.keys()):
            length = len(key)
            if length > 1:
                total = ""
                for i in range(length):
                    total += str(answer[key[i]][1])
                if len(str(total)) < len(str(answer[key][1])):
                    del answer[key]
    return answer

#Полный pipeline: очистка -> подсчёт подстрок -> отбор топ-N -> коды -> отсев
def build_codebook(text: str, top_n: int = 200) -> dict:
    words = clean(text)
    answer: dict = {}
    for word in words:
        razbr(word, answer)
    answer = dict(sorted(answer.items(), key=lambda item: item[1], reverse=True)[:top_n])
    answer = build(answer)
    answer = check(answer)
    return answer


if __name__ == "__main__":
    text = read_text()
    codebook = build_codebook(text)

    print(f"Подстрок в словаре: {len(codebook)}")
    print("\nПример (подстрока -> [частота, код]):")
    for key, val in list(codebook.items())[:15]:
        print(f"  {key!r:>20}  ->  {val}")