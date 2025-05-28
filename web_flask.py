from flask import Flask, request, render_template
from lexer import tokenize
from parser import Parser
from codegen import generate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    result = ""
    error = ""
    if request.method == "POST":
        code = request.form["code"]
        try:
            tokens = list(tokenize(code))
            parser = Parser(tokens)
            tree = parser.parse()
            result = generate(tree)
        except Exception as e:
            error = str(e)
    return render_template("index.html", code=code, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)