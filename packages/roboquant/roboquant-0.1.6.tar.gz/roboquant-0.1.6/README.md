
# Introduction
Roboquant is an open-source algorithmic trading platform. It is flexible, user-friendly and completely free to use. It is designed for anyone serious about algo-trading. So whether you are a beginning retail trader or an established trading firm, roboquant can help you to develop robust and fully automated trading strategies.

![roboquant logo](https://github.com/neurallayer/roboquant/raw/main/docs/roboquant_header.png)

# Install
Roboquant can be installed like most other Python packages, using for example pip or conda. Just make sure you have Python version 3.10 or higher installed.

```shell
python3 -m pip install --upgrade roboquant
```

If you want to use PyTorch based strategies and YahooFinance market data, you can install roboquant using the following command:

```shell
python3 -m pip install --upgrade roboquant[all]
```

# Usage
The following code snippet shows the code required to run a full back-test on a number of stocks.

```python
from roboquant import *

feed = YahooFeed("TSLA", "AMZN", "IBM")
strategy = EMACrossover()
roboquant = Roboquant(strategy)
tracker = StandardTracker()

roboquant.run(feed, tracker)
print(tracker)
```

# Building from source
Go to directory where you have downloaded the py_oboquant project and run the following commands to create a virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Now install the required packages and build roboquant in this virtual environment:

```shell
pip install -r requirements.txt
python -m build
```

To run the unittest:

```shell
python -m unittest discover -s tests/unit
```

To install it:

```shell
pip install .
```


## Interactive Brokers

Unfortunatly Interactive Brokers doesn't allow their Python client library to be redistributed by third parties. However it is freely available to be downloaded and installed. Please follow the instructions found [here](https://ibkrcampus.com/ibkr-quant-news/interactive-brokers-python-api-native-a-step-by-step-guide/) (download and install version 10.19).  

# Kotlin version
Next to this Python version of `roboquant`, there is also a Koltin version available. Both (will) share a similar API, just the used computer language is different.
Which one to use, depends very much on personal preference, skills and use-case.
