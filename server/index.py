from flask import Flask, request

app = Flask(__name__)


@app.route("/rateapp")
def index():
    with open("rates.txt", "r") as file:
        try:
            filer = file.read().split()
            count = int(filer[1])
            total = int(filer[2])
        except IndexError:
            print("EF")
            count = 0
            total = 0
    with open("rates.txt", "w") as file:
        file.write(str(float((int(request.args.get("rating")) + total) / (count + 1))) + " " + str(count + 1) + " " + str(int(request.args.get("rating")) + total))
    return "Success!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)