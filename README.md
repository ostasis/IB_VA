# Value averaging investing strategy with Interactive Brokers API

## Description

This "Sample" python script is designed to invest at set interval using [value averaging](https://www.investopedia.com/terms/v/value_averaging.asp) investing strategy. (Note this is done manually by running the script with IBKR TWS open).

## Limitations

- Using ASX stocks i.e. Australian (which you can edit)
- No code included to easily switch between Trading Account and Paper Trading
- No GUI
- Both TWS and the IB Gateway require daily restarts to refresh data and therefor will require you to login (if you're only investing monthly this isn't an issue)
- At this stage it uses [```MarketDataType 4```](https://interactivebrokers.github.io/tws-api/market_data_type.html) Delayed Frozen. Requests delayed "frozen" data for a user without market data subscriptions. It's free :)

## Contributing

To any of the above limitations; Perhaps a flask or django GUI. Please fork.

## Setup and install

1. Download and install [IBKR Trading API](http://interactivebrokers.github.io/)

2. Once installed create a new workspace in vscode within ```Python``` folder, found in ```~/IBJts/samples/Python``` and git clone this repo to there.

3. Open the file ```~/IBJts/samples/Python/Samples/algo-101-04-01.py``` within vscode and follow the steps below.

**Important, start in Paper Trading and switch to delta.seconds for testing**

4. Find the line below and ensure you are using Paper Trading

```app.connect("127.0.0.1", 7497, 1)  # 7496 Trading Account & 7497 Paper Account``` 

5. Also find the code block below and make changes necessary to trigger trades at your desired interval

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

6. Check out the API user guide and ensure you [enable API connections](https://interactivebrokers.github.io/tws-api/initial_setup.html).

7. The final step is to have TWS running in Paper Trading mode before executing ```~/IBJts/samples/Python/Samples/alog-101-04-01.py```.

8. Once you're satisfied with the results try actual trading **at your own risk, see LICENCE**.





