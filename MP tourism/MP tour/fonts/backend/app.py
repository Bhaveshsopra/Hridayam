from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/plan", methods=["POST"])
def plan():
    data=request.json
    name=data["name"]
    budget=int(data["budget"])

    if budget < 3000:
        result=f"{name}, you should visit local temples (low budget trip)"
    elif budget < 7000:
        result=f"{name}, visit Ujjain + Indore 2-day trip"
    else:
        result=f"{name}, full MP tour: Bhopal, Pachmarhi, Ujjain"

    return jsonify({"message":result})

app.run(debug=True)