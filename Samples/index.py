from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        form_data = request.form

        for x in form_data.to_dict():
            print(x)
            print(form_data.to_dict()[x])

        return render_template("data.html", form_data=form_data)


if __name__ == ("__main__"):
    app.run(debug=True)
