import urllib.request
import json
import csv
import os
from datetime import datetime, timezone


# ============================================================
# SETTINGS
# ============================================================

START_DATE = "2009-01-02"

OUTPUT_FOLDER = r"D:\prdp\Data Science\Live-Market\Historical"


# ============================================================
# DATE -> UNIX TIMESTAMP
# ============================================================

def date_to_timestamp(date_string):
    """
    Convert YYYY-MM-DD to Unix timestamp.
    """

    dt = datetime.strptime(date_string, "%Y-%m-%d")

    return int(dt.replace(tzinfo=timezone.utc).timestamp())


# ============================================================
# FETCH YAHOO HISTORICAL DATA
# ============================================================

def fetch_yahoo_history(ticker, start_date, end_date=None):

    start_timestamp = date_to_timestamp(start_date)

    if end_date is None:
        # Current date/time
        end_timestamp = int(datetime.now(timezone.utc).timestamp())
    else:
        end_timestamp = date_to_timestamp(end_date)

    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{ticker}"
        f"?period1={start_timestamp}"
        f"&period2={end_timestamp}"
        f"&interval=1d"
        f"&events=history"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/131.0 Safari/537.36"
        )
    }

    print(f"\nFetching {ticker}")
    print(f"Start : {start_date}")
    print(f"URL   : {url}")

    try:

        request = urllib.request.Request(
            url,
            headers=headers
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            raw_data = response.read().decode("utf-8")

        data = json.loads(raw_data)

        chart = data.get("chart", {})

        if chart.get("error"):
            raise ValueError(
                chart["error"]
            )

        result = chart.get("result")

        if not result:
            raise ValueError(
                f"No historical data returned for {ticker}"
            )

        result = result[0]

        timestamps = result.get("timestamp", [])

        quote_data = (
            result
            .get("indicators", {})
            .get("quote", [])
        )

        if not quote_data:
            raise ValueError(
                f"No quote data returned for {ticker}"
            )

        quote = quote_data[0]

        opens = quote.get("open", [])
        closes = quote.get("close", [])

        rows = []

        for i, timestamp in enumerate(timestamps):

            date = datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc
            ).strftime("%Y-%m-%d")

            open_price = (
                opens[i]
                if i < len(opens)
                else None
            )

            close_price = (
                closes[i]
                if i < len(closes)
                else None
            )

            # Skip rows where Open or Close is unavailable
            if open_price is None or close_price is None:
                continue

            rows.append({
                "Date": date,
                "Open": float(open_price),
                "Close": float(close_price)
            })

        return rows

    except Exception as e:

        raise RuntimeError(
            f"Failed to fetch {ticker}: {e}"
        )


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(rows, filename):

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    file_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Header
        writer.writerow([
            "Date",
            "Open",
            "Close"
        ])

        # Data
        for row in rows:

            writer.writerow([
                row["Date"],
                f'{row["Open"]:.6f}',
                f'{row["Close"]:.6f}'
            ])

    print(
        f"Saved {len(rows):,} rows -> {file_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # GOLD BEES
    # --------------------------------------------------------

    gold_data = fetch_yahoo_history(
        ticker="GOLDBEES.NS",
        start_date=START_DATE
    )

    save_csv(
        gold_data,
        "GOLDBEES_Historical_Daily.csv"
    )


    # --------------------------------------------------------
    # SILVER BEES
    # --------------------------------------------------------

    silver_data = fetch_yahoo_history(
        ticker="SILVERBEES.NS",
        start_date=START_DATE
    )

    save_csv(
        silver_data,
        "SILVERBEES_Historical_Daily.csv"
    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n======================================")
    print("DOWNLOAD COMPLETE")
    print("======================================")

    print(
        f"Gold BeES   : {len(gold_data):,} records"
    )

    print(
        f"Silver BeES : {len(silver_data):,} records"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
