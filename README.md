# IB_VA
## Value Averaging with Interactive Brokers API

### Setup and install

Download and install [IBKR Trading API](http://interactivebrokers.github.io/)

Once installed create a new workspace in vscode from "Python" folder, found in ~/IBJts/samples/Python and git clone this repo to there.

Open the file ~/IBJts/samples/Python/Samples/alog-101-04-01.py within vscode and follow steps below.

#### Important, start in Paper Trading and switch to delta.seconds for testing
Find the line 

```app.connect("127.0.0.1", 7497, 1)  # 7496 Trading Account & 7497 Paper Account and ensure you are using Paper Trading```

Also find the code block below
```
delta_check = (
    delta.days
)  # delta.seconds (switch to delta.seconds for testing in Paper Trading)
weekday = d1.strftime("%A")

if not (
    d1.day >= 10
    and (
        weekday == "Monday"
        or weekday == "Tuesday"
        or weekday == "Wednesday"
        or weekday == "Thursday"
        or weekday == "Friday"
    )
    and d1.hour >= 11
    and delta_check
    >= 21  # >= 21 days, change to 5*60 if using delta.seconds in Paper Trading to run every 5 minutes.
):
```

Check out the API user guide and ensure you [enable API connections](https://interactivebrokers.github.io/tws-api/initial_setup.html)





