# Value averaging investing strategy with Interactive Brokers API

## Description

The "Samples" python script is designed to invest at set interval using [value averaging](https://www.investopedia.com/terms/v/value_averaging.asp) investing strategy. (Note this is done manually by running the script with IBKR TWS open).

## Reason

- IBKR margin rates are good
- A lot of trading platform API's don't work for Australia shares
- QuantConnect for example doesn't recognise ASX shares when live trading with Interactive Brokers
- Other examples are TD Ameritrade and Alpaca
- I use this myself to invest monthly using VA strategy

## Limitations

- Using ASX stocks i.e. Australian (which you can edit)
- No code to switch between DCA and Value Averaging
- No stop loss functionality
- No error capture or logging
- Both TWS and the IB Gateway require daily restarts to refresh data and therefor will require you to login (if you're only investing monthly this isn't an issue)
- At this stage it uses [```MarketDataType 4```](https://interactivebrokers.github.io/tws-api/market_data_type.html); Delayed Frozen. Requests delayed "frozen" data for a user without market data subscriptions.
- I would like to see if someone could create a pinescript for Trading View to do the same thing.


## Contributing

To any of the above limitations.

## Setup and install

1. Download and install [IBKR Trading API](http://interactivebrokers.github.io/)

2. Once installed create a new workspace in vscode within ```Python``` folder, found in ```~/IBJts/samples/Python``` and git clone this repo to there.

**Important, start in Paper Trading for testing**

3. Have TWS running in Paper Trading

4. Check out the API user guide and ensure you [enable API connections](https://interactivebrokers.github.io/tws-api/initial_setup.html).

5. From vscode terminal ```~/IBJts/samples/Python/Samples/$ python3 -c 'import algo; algo.invest(7497,0,700,3250)'``` 7497, is the paper trading account. 0, will wait 0 days to invest again and will invest every 60 seconds. 700, is the minimum amount to invest per asset. 3250, will invest $3250 every 60 seconds.

6. Once you're satisfied it works try using the gui to invest from. To do this have TWS running in paper trading account and from vscode terminal ```~/IBJts/samples/Python/Samples/$ python3 tkinter-app.py```. I recommend you stay in paper trading mode.

7. Before trying actual trading please review the following lines 372-278 in ```~/IBJts/samples/Python/Samples/alog.py``` see below:

            if not (  # you can add your own restrictions in here i.e. invest after the 10th on every Monday after 11am
                # d1.day >= 10
                # and weekday == "Monday"
                # and d1.hour >= 11
                delta_check
                >= recurring_interval
            ):

8. Once you're satisfied with the results try actual trading **at your own risk, see LICENCE**. 





