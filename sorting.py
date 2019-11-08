from flask import Flask, render_template, redirect, request
from utilities import build_data, parse_data, generate_quiz

# create a Flask objec called app
app = Flask(__name__, static_url_path='')

@app.route("/")
def home():
	return render_template('sortinghat.html')

@app.route("/start")
def start():
    easter = request.args.get("e") == "true"

    # Create the base score
    begin_score = {
        "iat": 0.0,
        "se": 0.0,
        "bdam": 0.0,
        "fict": 0.0
    }

    # Build the initial data
    begin_data = build_data(begin_score)

    # Forward to first question
    return redirect('/question?step=0&data=' + begin_data + '&e=' + str(easter).lower())

@app.route("/question")
def question():
    step = int(request.args.get("step"))
    data = request.args.get("data")
    easter = request.args.get("e")

    # Parse the current meta data
    score = parse_data(data)

    # Pull the quiz data
    quiz = generate_quiz()
    question = quiz[step]
    
    # Create the template context
    context = {
        "score": score,
        "step": step,
        "question": question['question'],
        "answers": question['answers'],
        "easteregg": easter == "true",
        "progress": ((step / 15) * 100)
    }

    return render_template('question.html', **context)

@app.route("/forward")
def forward():
    step = int(request.args.get("step"))
    data = request.args.get("data")
    option = request.args.get("option")
    weight = request.args.get("weight")
    easter = request.args.get("e")

    # Parse the current meta data
    score = parse_data(data)

    # Increment the step
    step += 1

    # Update the score
    score[option] += float(weight)

    # Build a new score string
    new_score = build_data(score)

    # Forward to result page
    if step >= len(generate_quiz()):
        # Create a list of answers
        answers = []

        for value, score in score.items():
            answers.append((value, score))
        
        # Sort the results
        answers.sort(key=lambda item: -item[1])

        # Retrieve the result
        result = answers[0][0]

        if easter:
            return redirect('/result?v=' + result + "&data=" + new_score + '&e=true')
        else:
            return redirect('/result?v=' + result + "&data=" + new_score)

    # Forward to the new question
    if easter:
        return redirect('/question?step=' + str(step) + '&data=' + new_score + '&e=true')
    else:
        return redirect('/question?step=' + str(step) + '&data=' + new_score)

@app.route("/result")
def result():
    value = request.args.get("v")
    data = request.args.get('data')
    easter = request.args.get("e")
    result = "Onbekend"
    summary = "Onbekend"

    # Parse the current meta data
    score = parse_data(data)

    # Build the texts
    if value == "iat":
        result = "Interactie-technologie"
        summary = "Als IAT'er ben jij goed in het ontwerpen en bouwen van grafische of fysieke interfaces met een oog voor hoe gebruikers het programma ervaren en de skills om snel een werkend prototype op te zetten"
    elif value == "bdam":
        result = "Business Data Management"
        summary = "Als BDAM'er ben jij een nieuwsgierige en analytisch ingestelde persoon. Als data-detective ga je op zoek naar verborgen patronen in de data en richt je je op het ontwerpen en realiseren van data-oplossingen"
    elif value == "se":
        result = "Software Engineering"
        summary = "Als SE'er kan jij goed structuur aanbrengen in een applicatie door de toepassing van functies en een algoritme ontwikkelen met gebruik van expressies, variabelen, condities en conditionele statements, iteraties, datastructuren en standaardbibliotheken"
    elif value == "fict":
        result = "Forensisch ICT"
        summary = "Als FICT'er ben jij goed in het objectief uitvoeren van een technisch onderzoek met een oog voor belangrijke details en de benodigde skills om je onderzoek goed te rapporteren"

    # Build the context
    context = {
        "result": result,
        "easteregg": easter == "true",
        "summary": summary,
        "results": "[{0},{1},{2},{3}]".format(score['iat'], score['bdam'], score['se'], score['fict'])
    }

    return render_template('result.html', **context)

if __name__ == "__main__":
	app.run('localhost', port=8082, debug=True)
