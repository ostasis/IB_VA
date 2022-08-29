from flask import Flask, render_template, request


class Test:
    def __init__(self) -> None:
        self.amount = 1000


app = Test()


def do_something_now():
    print("your shitting me")


flask_app = Flask(__name__)


@flask_app.route("/")
@flask_app.route("/form")
def form():
    return render_template("form.html")


@flask_app.route("/data", methods=["POST", "GET"])
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
            if x == "Amount":
                app.amount = form_data.to_dict()[x]

        print(app.amount)

        do_something_now()

        return render_template("data.html", form_data=form_data)


if __name__ == ("__main__"):
    flask_app.run(debug=True)

