# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def sredball(marksstr, ballstr):
    try:
        marks = [int(i) for i in marksstr.split()]
        avg = float(ballstr)
        slov = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # Словарь с колличеством каждой оценки, которое нужно будет получить
        summa = sum(marks)  # Сумма оценок
        lenn = len(marks)  # Колличесвто оценок
        your_avg = float(str(summa / lenn)[:4])  # Подсчитываем нынешний средний балл
        marks = [5, 4, 3, 2, 1]
        vivod = []
        vivodstr = str(
            'Ваш средний балл: ' + str(your_avg) + '. Для достижения требуемого среднего балла вам нужно получить:')
        if avg > 5:
            return 'Введенный требуемый средний балл не коректен.'

        if your_avg >= avg:
            return str('Ваш средний балл: ' + str(
                your_avg) + '. Требуемый средний балл уже достигнут. Продолжайте получать хорошие оценки! ;)')

        if avg == 5 and your_avg != 5:
            return str(
                'Ваш средний балл: ' + str(your_avg) + ', к сожалению, вы не сможете достигнуть требуемого балла. :(')

        if avg == 0 and your_avg != 0:
            return str(
                'Ваш средний балл: ' + str(your_avg) + ', к сожалению, вы не сможете достигнуть требуемого балла. :(')

        for i in range(int(5 - avg // 1)):

            ocenka = marks[i]

            summa_plus = 0  # Сумма оценок, которые мы прибавим
            lenn_plus = 0  # Сколько оценок мы прибавим
            avgg = your_avg  # Средний балл, который будет изменяться для цикла

            while avgg <= avg:  # Прибавляем оценку и получаем новый средний балл,сравниваем с требуемым

                slov[ocenka] += 1
                summa_plus += ocenka
                lenn_plus += 1
                avgg = (summa + summa_plus) / (lenn + lenn_plus)

        for i in slov:
            if slov[i] != 0:
                vivod.append((i, slov[i]))

        for i in vivod:
            vivodstr += str('\n' + str(i[0]) + ' в колличестве ' + str(i[1]))

        return vivodstr

    except Exception:
        return 'Ввод не корректен. '


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:

        sessionStorage[user_id] = {
            'suggests': [
                "Привет",
                "Помощь",
            ]
        }

        res['response'][
            'text'] = 'Привет! Я подскажу тебе, какие оценки ты должен получить для' \
                      ' достижения желаемого среднего балла. Сначала скажи средний' \
                      ' балл, который хочешь получить, а потом свои текущие оценки.' \
                      ' Вот так: 4.6  4 5 4 5'

        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что ты умеешь?',
        'помоги',
    ]:
        res['response']['text'] = 'Я подскажу какие оценки тебе нужно получить, чтобы достичь ' \
                                  'желаемого балла. Просто введи сначала ' \
                                  'балл, который хочешь получить, а потом свои текущие оценки. ' \
                                  'Пример: 4.7 3 4 2 4 5 4'
        return


    if req['request']['original_utterance'].lower() == 'какая оценка за проект?':
        res['response']['text'] = '5'
        return

    if req['request']['original_utterance'].lower() == 'сайт':
        res['response']['text'] = 'Можете перейти по ссылке: mionitsa.pythonanywhere.com '
        return

    if req['request']['original_utterance'].lower() == 'привет':
        res['response']['text'] = 'Привет, друг!'
        return

    if req['request']['original_utterance'].lower() == 'пока':
        res['response']['text'] = 'Миша пока('
        return

    sred = req['request']['original_utterance'].split()[0].replace(',', '.')
    sred2 = []
    for i in sred:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            sred2.append(i)
    sred = sred2[0] + '.' + ''.join(sred2[1:])

    marks = ''.join(req['request']['original_utterance'].split()[1:])
    marks2 = []
    for i in marks:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            marks2.append(i)
    marks = ' '.join(marks2)

    res['response']['text'] = sredball(marks, sred)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests.append({
        "title": "сайт",
        "url": "https://mionitsa.pythonanywhere.com",
        "hide": False
    })

    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests']
    ]


    return suggests
