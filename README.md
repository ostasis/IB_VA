# Value Averaging with Interactive Brokers API

## Description

This "Sample" python script is designed to invest at set interval (note this is done manually by running the script with IBKR TWS open) using [value averaging](https://www.investopedia.com/terms/v/value_averaging.asp)

## Limitations

- Using ASX stocks
- No code included to easily switch between Trading Account and Paper Trading
- No GUI


## Contributing





### Setup and install

Download and install [IBKR Trading API](http://interactivebrokers.github.io/)

Once installed create a new workspace in vscode from ```Python``` folder, found in ```~/IBJts/samples/Python``` and git clone this repo to there.

Open the file ```~/IBJts/samples/Python/Samples/alog-101-04-01.py``` within vscode and follow steps below.

** Important, start in Paper Trading and switch to delta.seconds for testing **
Find the line below and ensure you are using Paper Trading

```app.connect("127.0.0.1", 7497, 1)  # 7496 Trading Account & 7497 Paper Account``` 

Also find the code block below and make changes necessary to trigger trades at your desired interval

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

The final step is to have TWS running in Paper Trading mode before executing ```~/IBJts/samples/Python/Samples/alog-101-04-01.py```

Once you're satisfied with the results try actual trading at your own risk, see disclamer below.

DISCLAIMER OF DAMAGES. (a) TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT WILL LICENSOR OR ITS AFFILIATES, LICENSORS, SUPPLIERS OR RESELLERS BE LIABLE TO LICENSEE UNDER ANY THEORY FOR ANY DAMAGES SUFFERED BY LICENSEE OR ANY USER OF SOFTWARE, OR FOR ANY SPECIAL, INCIDENTAL, IN- DIRECT, CONSEQUENTIAL, OR SIMILAR DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES FOR LOSS OF PROFITS OR CONFIDENTIAL OR OTHER INFORMATION, FOR BUSINESS INTERRUPTION, FOR PER- SONAL INJURY, FOR LOSS OF PRIVACY, FOR FAILURE TO MEET ANY DUTY INCLUDING OF GOOD FAITH OR OF REASONABLE CARE, FOR NEGLIGENCE, AND FOR ANY OTHER PECUNIARY OR OTHER LOSS WHATSO- EVER) ARISING OUT OF THE USE OR INABILITY TO USE SOFTWARE, OR THE PROVISION OF OR FAILURE TO PROVIDE SUPPORT SERVICES, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES, AND REGARDLESS OF THE LEGAL OR EQUITABLE THEORY (CONTRACT, TORT OR OTHERWISE) UPON WHICH THE CLAIM IS BASED.





