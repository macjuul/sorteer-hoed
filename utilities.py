import xlrd
import base64
import json
import urllib
 
# Parse a data string into a dict
def parse_data(data_str):
    url_str = urllib.parse.unquote(data_str)

    data_json = str(base64.b64decode(url_str.encode('utf-8')), 'utf-8')
    return json.loads(data_json)

# Build a data string from a dict
def build_data(data):
    data_json = json.dumps(data)
    data_b64 = str(base64.b64encode(data_json.encode('utf-8')), 'utf-8')
    res = urllib.parse.quote(data_b64)

    return res

def generate_quiz():
    quiz = []

    # Open the database
    locatie = (r'./database.xlsx')
    werkboek = xlrd.open_workbook(locatie)
    sheet_count = len(werkboek.sheets())

    for i in range(0, sheet_count - 6):
        sheet = werkboek.sheet_by_index(i)
        question = sheet.cell_value(1, 0)
        answers = []

        for y in range(1, 5):
            text = sheet.cell_value(y, 1)
            weight = sheet.cell_value(y, 2)
            value = sheet.cell_value(y, 3)

            answers.append({
                "text": text,
                "weight": int(weight),
                "value": value
            })

        quiz.append({
            "question": question,
            "answers": answers
        })

    # For now simply insert the colors
    for question in quiz:
        question['answers'][0]['color'] = "green"
        question['answers'][1]['color'] = "gold"
        question['answers'][2]['color'] = "blue"
        question['answers'][3]['color'] = "red"

    return quiz