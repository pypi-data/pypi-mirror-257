# krakenohlcvt

A python package to handle Kraken exchange historial OHLCVT data without needing to unzip the Kraken_OHLCVT.zip file.

# Installation

```bash
pip install krakenohlcvt
```

or

```bash
potry add krakenohlcvt
```

# Usage

```python

from krakenohlcvt import KrakenDataHandler


# Enter path to the Kraken zip file:

import os

DATA_PATH = os.path.expanduser("~/Downloads/Kraken_OHLCVT.zip")

# or simpler:

DATA_PATH = "path/to/Kraken_OHLCVT.zip"


# load it

kd = KrakenDataHandler(DATA_PATH)


# you can inspect which symbols it contains:
kd.list_symbols()

# when searching for a specific symbol, search with either "starts_with=" or "contains="
kd.list_symbols(starts_with="ETH")

# then get the timeframe from the specific symbol
df = kd.load_symbol_data("ETHUSDT", "15m")
# if timeframe not in ["1m", "15m", "1h", "1d"], then the '1m' data gets loaded and the timeframe
# inferred from the 1m data!


# save a timeframe of a specific symbol as df pickle:
kd.save_to_df_pickle(symbol="ETHUSDT", timeframe="15m", outpath=os.path.expanduser("~/projects/python/LotusBot/src/backtester/ETHUSDT_15m.csv"), dropna_rows=True)

# convert unix time in the index to human-readable datetime object
[kd.unix_to_datetime(x) for x in df.index] # very slow! a lot faster:
kd.unix_to_datetime(df.index)
# also possible
[datetime.datetime.fromtimestamp(x) for x in df.index]

```

