import os.path
import threading
import time
from datetime import datetime as dt
from datetime import timedelta as td
from threading import Timer


import numpy as np
import pandas as pd
from ibapi.client import EClient
from ibapi.common import TickerId
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import EWrapper


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        # https://stackoverflow.com/questions/57618971/how-do-i-get-my-accounts-positions-at-interactive-brokers-using-python-api

        self.all_positions = pd.DataFrame(
            [], columns=["Account", "Symbol", "Quantity", "Average Cost", "Sec Type"]
        )
        # self.all_positions["Average Cost"].astype(float)
        # self.all_positions.convert_dtypes(convert_floating=True)

        self.all_accounts = pd.DataFrame(
            [], columns=["reqId", "Account", "Tag", "Value", "Currency"]
        )
        # self.all_accounts.convert_dtypes(convert_floating=True)

        """ my stuff, fingers crossed """

        self.amount = 2500  # amount to invest monthly
        # self.filled = False

        self.Cushion = 1.0

        if not os.path.exists("portfolio.xlsx"):
            # change symbols and weightings to your preferences below
            # once portfolio.xlsx is generated the first time this will be ignored and changes will need to be made directly.
            # Note this requires having index/symbol, Weight and Last Date filled in
            self.symbols = {
                "VHY": {
                    "Weight": 0.00
                },  # Aims for exposure to companies with higher forecast dividends relative to other ASX-listed companies.
                "VAS": {"Weight": 0.50},  # Tracks the return of the S&P/ASX 300 Index.
                "VGS": {
                    "Weight": 0.20
                },  # Exposure to many of the world’s largest companies (ex-Australia) with net dividends reinvested.
                "ETHI": {
                    "Weight": 0.20
                },  # ETHI aims to track the performance of an index (before fees and expenses) that includes a portfolio of large global stocks identified as “Climate Leaders”
                "NDQ": {
                    "Weight": 0.10
                },  # NDQ aims to track the performance of the NASDAQ-100 Index (before fees and expenses)
            }
            self.df = pd.DataFrame.from_dict(self.symbols, orient="index")
            for index, row in self.df.iterrows():

                self.df.at[index, "Target Amount"] = 0.0
                # self.df.at[index, "Actual Weight"] = 0.0
                self.df.at[index, "Actual Amount"] = 0.0
                self.df.at[index, "Total Quantity"] = 0.0
                # self.df.at[index, "Total Value"] = 0.0
                self.df.at[index, "Average Price"] = 0.0
                self.df.at[index, "Last avgFillPrice"] = None
                self.df.at[index, "Last filled"] = None
                # self.df.at[index, "Last Amount"] = None
                self.df.at[index, "Last Date"] = dt.now() - td(
                    days=30
                )  # init the date to be 30 days ago
        else:
            self.df = pd.read_excel("portfolio.xlsx", index_col=0)
            # self.df.convert_dtypes(convert_floating=True)
            self.df.to_excel(
                f"portfolio_{dt.now().year}_{dt.now().month}_{dt.now().day}.xlsx"
            )
        pd.set_option("display.max_columns", None)

    """ end my stuff, fingers crossed """

    # https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print(
            '############## app.connect("127.0.0.1", 7497, 1)  # 7496 Trading Account & 7497 Paper Account  ##############'
        )
        print(
            "############## delta.seconds, is useful for testing under paper trading.   ##############"
        )
        print(
            "############## YOU HAVE 60 SECONDS TO CANCEL, TEST IN PAPER TRADING FIRST. ##############"
        )

        print("The next valid order id is: ", self.nextorderId)

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ):
        print(
            "orderStatus - orderid:",
            orderId,
            "status:",
            status,
            "filled",
            filled,
            "remaining",
            remaining,
            "avFillPrice",
            avgFillPrice,
            "lastFillPrice",
            lastFillPrice,
        )
        # try this out tomorrow need to add orderId to df
        index = self.df.index[self.df["orderId"] == orderId].tolist()[0]
        self.df.at[index, "Last Date"] = dt.now()
        if status == "Filled":
            self.df.at[index, "Last avgFillPrice"] = avgFillPrice
            self.df.at[index, "Last filled"] = filled
            # self.df.at[index, "Last Amount"] = filled * avgFillPrice
            # self.filled = True
        self.df.to_excel("portfolio.xlsx")

    def openOrder(self, orderId, contract, order, orderState):
        print(
            "openOrder id:",
            orderId,
            contract.symbol,
            contract.secType,
            "@",
            contract.exchange,
            ":",
            order.action,
            order.orderType,
            order.totalQuantity,
            orderState.status,
        )

    def execDetails(self, reqId, contract, execution):
        print(
            "Order Executed: ",
            reqId,
            contract.symbol,
            contract.secType,
            contract.currency,
            execution.execId,
            execution.orderId,
            execution.shares,
            execution.lastLiquidity,
        )

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        if reqId > -1:
            print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

    def position(self, account, contract, pos, avgCost):
        index = str(contract.symbol)
        self.all_positions.loc[index] = (
            account,
            contract.symbol,
            pos,
            avgCost,
            contract.secType,
        )

    def accountSummary(self, reqId, account, tag, value, currency):
        index = str(account)
        self.all_accounts.loc[index] = reqId, account, tag, value, currency

        print(f"{tag}: {value}")

        if tag == "Cushion":
            self.Cushion = float(value)

    def tickPrice(self, reqId, tickType, price, attrib):
        print(
            "Tick Size. Ticker Id: ",
            reqId,
            "tickType: ",
            TickTypeEnum.to_str(tickType),
            "Price: ",
            price,
            end="\n",
        )

        if tickType == 69:  # 0:
            self.df.at[self.df.index[reqId - 1], "Bid_Size"] = price

        if tickType == 66:  # 1:
            self.df.at[self.df.index[reqId - 1], "Bid_Price"] = price

        if tickType == 67:  # 2:
            self.df.at[self.df.index[reqId - 1], "Ask_Price"] = price

        if tickType == 70:  # 3:
            self.df.at[self.df.index[reqId - 1], "Ask_Size"] = price

        if tickType == 68:  # 4:
            self.df.at[self.df.index[reqId - 1], "Last_Price"] = price

        if tickType == 71:  # 5:
            self.df.at[self.df.index[reqId - 1], "Last_Size"] = price

        if tickType == 72:  # 6:
            self.df.at[self.df.index[reqId - 1], "High"] = price

        if tickType == 73:  # 7:
            self.df.at[self.df.index[reqId - 1], "Low"] = price

        if tickType == 74:  # 8:
            self.df.at[self.df.index[reqId - 1], "Volume"] = price

        if tickType == 75:  # 9:
            self.df.at[self.df.index[reqId - 1], "Close_Price"] = price

        self.df.to_excel("portfolio.xlsx")

    def tickSize(self, reqId, tickType, size):
        print(
            "Tick Size. Ticker Id: ",
            reqId,
            "tickType: ",
            TickTypeEnum.to_str(tickType),
            "Size: ",
            size,
            end="\n",
        )

    def historicalData(self, reqId: int, bar):
        print(
            "HistoricalData: ",
            reqId,
            "Date: ",
            bar.date,
            "Open: ",
            bar.open,
            "High: ",
            bar.high,
            "Low: ",
            bar.low,
            "Close: ",
            bar.close,
            "Volume: ",
            bar.volume,
            "Count: ",
            bar.barCount,
        )


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def run_loop():
    app.run()


# Function to create STK Order contract
def STK_order(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "AUD"
    contract.exchange = "SMART"
    contract.primaryExchange = "ASX"
    return contract


""" 
def liquidate_all_positions():
    app.reqPositions()  # associated callback: position
    print("Waiting for IB's API response for accounts positions requests...\n")
    time.sleep(1)
    current_positions = app.all_positions
    print(current_positions)

    for index, row in current_positions.iterrows():

        # Create order object
        order = Order()
        order.action = "SELL"
        order.totalQuantity = row["Quantity"]
        order.orderType = "MKT"

        # Place order
        app.placeOrder(app.nextorderId, STK_order(row["Symbol"]), order)
        app.nextorderId += 1

        time.sleep(1)

        # Cancel order
        print("cancelling order")
        app.cancelOrder(app.nextorderId)
"""

"""WARNING: MAKE SURE YOU UNDERSTAND THE RISKS AND DIFFERNCES BETWEEN 7496 Trading Account & 7497 Paper Account"""
app = IBapi()
app.connect("127.0.0.1", 7496, 1)  # 7496 Trading Account & 7497 Paper Account

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()


def summary():
    tags = [
        "AccountType",
        "NetLiquidation",
        "TotalCashValue",
        "SettledCash",
        "AccruedCash",
        "BuyingPower",
        "EquityWithLoanValue",
        "PreviousDayEquityWithLoanValue",
        "GrossPositionValue",
        "ReqTEquity",
        "ReqTMargin",
        "SMA",
        "InitMarginReq",
        "MaintMarginReq",
        "AvailableFunds",
        "ExcessLiquidity",
        "Cushion",
        "FullInitMarginReq",
        "FullMaintMarginReq",
        "FullAvailableFunds",
        "FullExcessLiquidity",
        "LookAheadNextChange",
        "LookAheadInitMarginReq",
        "LookAheadMaintMarginReq",
        "LookAheadAvailableFunds",
        "LookAheadExcessLiquidity",
        "HighestSeverity",
        "DayTradesRemaining",
        "Leverage",
    ]
    reqId = 0
    for t in tags:
        app.reqAccountSummary(reqId, "All", t)
        if reqId == 0:
            reqId = 1
            continue
        else:
            reqId = 0
            time.sleep(1)

    return


def dummyfn():

    # Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            # print("connected")
            break
        else:
            # print("waiting for connection")
            time.sleep(2)

    time.sleep(1)  # Sleep interval to allow time for connection to server

    current_time = dt.now()
    sum_target_amount = app.df[
        "Target Amount"
    ].sum()  # sum of target amount for rebalance month

    for index, row in app.df.iterrows():
        if (
            current_time is not None
            and app.df.at[index, "Last Date"] is not None
            # and row["Weight"] > 0.0
        ):

            d0 = app.df.at[index, "Last Date"]  # app.buy_time
            d1 = current_time
            delta = d1 - d0
            delta_check = (
                delta.days
            )  # delta.seconds (switch to delta.seconds for testing in Paper Trading)
            weekday = d1.strftime("%A")

            if not (
                d1.day >= 10
                and (weekday == "Monday")
                and d1.hour >= 11
                and delta_check
                >= 21  # >= 21 days, change to 5*60 if using delta.seconds in Paper Trading to run every 5 minutes.
            ):
                continue
            else:

                row_number = app.df.index.get_loc(index) + 1

                if row_number == 1:
                    summary()
                    # IB margin is about 0.2 therefore 0.5 would mean $1 for $1 investing, less than that would mean too much leverage for me ;)
                    if app.Cushion <= 0.5:  # reached Margin Cushion therefore return
                        print(
                            f"Margin Cushion of less than 0.5 reached. Cushion: {app.Cushion}"
                        )
                        return
                    else:
                        print(f"Investing Time. Cushion: {app.Cushion}")
                        print(app.df)

                # return  # here during testing to avoid trade and updating xlsx

                contract = STK_order(index)

                app.reqMarketDataType(
                    4
                )  # switch to delayed frozen data if live is not available
                app.reqMktData(row_number, contract, "", True, False, [])
                time.sleep(11)

                # Below if statement is in decending order of the best way to get price to calculate order.totalQuantity
                if (
                    "Ask_Price" in app.df.columns
                    and "Last_Price" in app.df.columns
                    and "Close_Price" in app.df.columns
                ):
                    if not (
                        app.df.at[index, "Ask_Price"] == -1
                        or np.isnan(app.df.at[index, "Ask_Price"])
                    ):
                        price = app.df.at[index, "Ask_Price"]
                        print("###### ask ######")
                    elif not (
                        app.df.at[index, "Last_Price"] == -1
                        or np.isnan(app.df.at[index, "Last_Price"])
                    ):
                        price = app.df.at[index, "Last_Price"]
                        print("###### last ######")
                    elif not (
                        app.df.at[index, "Close_Price"] == -1
                        or np.isnan(app.df.at[index, "Close_Price"])
                    ):
                        price = app.df.at[index, "Close_Price"]
                        print("###### close ######")
                    else:
                        print("no price available")
                        continue
                else:
                    print("market data not returned")
                    continue

                time.sleep(1)

                app.reqPositions()  # associated callback: position
                print(
                    "Waiting for IB's API response for accounts positions requests...\n"
                )
                time.sleep(1)
                current_positions = app.all_positions
                print(current_positions)

                for index1, row1 in current_positions.iterrows():
                    print(f"index: {index1}")
                    print(f"row: {row1}")
                current_symbols = current_positions.index.tolist()
                if index in current_symbols:
                    app.df.at[index, "Total Quantity"] = current_positions.at[
                        index, "Quantity"
                    ]
                    app.df.at[index, "Average Price"] = current_positions.at[
                        index, "Average Cost"
                    ]

                ##### VA #####

                app.df.at[index, "Actual Amount"] = (
                    price * app.df.at[index, "Total Quantity"]
                )
                # If starting xlsx from scratch set target to actual to avoid selling stk's
                if app.df.at[index, "Target Amount"] == 0:
                    app.df.at[index, "Target Amount"] = app.df.at[
                        index, "Actual Amount"
                    ]

                if not d1.month == 8:  # rebalance in this month
                    app.df.at[index, "Target Amount"] += row["Weight"] * app.amount
                else:
                    app.df.at[index, "Target Amount"] = (
                        sum_target_amount * row["Weight"]
                    ) + (row["Weight"] * app.amount)

                amount_delta = (
                    app.df.at[index, "Target Amount"]
                    - app.df.at[index, "Actual Amount"]
                )

                app.df.at[index, "Last Date"] = dt.now()
                app.df.to_excel("portfolio.xlsx")
                time.sleep(1)

                # Create order object
                order = Order()

                order.totalQuantity = int((amount_delta) / price) + (
                    (amount_delta) % price > 0
                )

                if order.totalQuantity == 0:
                    print(app.df)
                    continue
                elif order.totalQuantity >= 1:
                    order.action = "BUY"
                else:  # will this add up last amount correctly may need to store last order action
                    order.totalQuantity = abs(order.totalQuantity)
                    order.action = "SELL"

                # fees approx. $7 per trade therefor let amount_delta build up to greater than $700 to pay 1% fees.
                if amount_delta < 700:
                    print(app.df)
                    continue

                order.orderType = "MKT"

                app.df.at[index, "orderId"] = app.nextorderId

                time.sleep(1)

                # Place order
                app.placeOrder(app.nextorderId, STK_order(index), order)

                time.sleep(1)

                app.nextorderId += 1

            # print(f'Actual amount invested: ${app.df["Last Amount"].sum()}')

            time.sleep(11)

            print(app.df)

            # app.df.to_excel("portfolio.xlsx")

    return


timer = RepeatTimer(60, dummyfn)  # keep connection alive every 60 seconds
timer.start()
time.sleep(20 * 60 * 60)  # will run for 24 hours
timer.cancel()

"""WARNING: MAKE SURE YOU UNDERSTAND THE RISKS OF UNCOMMENTING THE BELOW LINE
        Only uncomment this line in Paper Trading mode
        This is useful if you run out of funds whilst testing
        Do no uncommnet in Actual Trading because as it says it will liquidate all of your positions
        Additionally you would comment out the 4 code lines above otherwise you'll be waiting 20 hours and also uncomment the function itself"""
####### liquidate_all_positions()

time.sleep(1)
app.disconnect()
