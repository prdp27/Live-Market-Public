# import csv
# import os
#
#
# # ============================================================
# # FOLDER
# # ============================================================
#
# FOLDER = r"D:\prdp\Data Science\Live-Market"
#
#
# # ============================================================
# # INPUT FILES
# # ============================================================
#
# GOLD_OPEN_FILE = os.path.join(
#     FOLDER,
#     "EFT-GOLDBEES_Open.csv"
# )
#
# GOLD_CLOSE_FILE = os.path.join(
#     FOLDER,
#     "EFT-GOLDBEES_Close.csv"
# )
#
# SILVER_OPEN_FILE = os.path.join(
#     FOLDER,
#     "EFT-SILVERBEES_Open.csv"
# )
#
# SILVER_CLOSE_FILE = os.path.join(
#     FOLDER,
#     "EFT-SILVERBEES_Close.csv"
# )
#
#
# # ============================================================
# # OUTPUT FILES
# # ============================================================
#
# GOLD_OUTPUT = os.path.join(
#     FOLDER,
#     "EFT-GOLDBEES_Stacked.csv"
# )
#
# SILVER_OUTPUT = os.path.join(
#     FOLDER,
#     "EFT-SILVERBEES_Stacked.csv"
# )
#
#
# # ============================================================
# # READ OPEN / CLOSE FILE
# # ============================================================
#
# def read_price_file(file_path, price_column):
#
#     data = {}
#
#     with open(
#         file_path,
#         "r",
#         newline="",
#         encoding="utf-8-sig"
#     ) as file:
#
#         reader = csv.DictReader(file)
#
#         for row in reader:
#
#             date = row["Date"].strip()
#             price = row[price_column].strip()
#
#             if date and price:
#
#                 data[date] = price
#
#     return data
#
#
# # ============================================================
# # STACK OPEN + CLOSE BY DATE
# # ============================================================
#
# def create_stacked_file(
#     open_file,
#     close_file,
#     output_file
# ):
#
#     # --------------------------------------------------------
#     # Read Open
#     # --------------------------------------------------------
#
#     open_data = read_price_file(
#         open_file,
#         "Open"
#     )
#
#     # --------------------------------------------------------
#     # Read Close
#     # --------------------------------------------------------
#
#     close_data = read_price_file(
#         close_file,
#         "Close"
#     )
#
#     # --------------------------------------------------------
#     # Combine all dates
#     # --------------------------------------------------------
#
#     all_dates = set()
#
#     all_dates.update(
#         open_data.keys()
#     )
#
#     all_dates.update(
#         close_data.keys()
#     )
#
#     # --------------------------------------------------------
#     # Sort dates
#     # --------------------------------------------------------
#
#     sorted_dates = sorted(
#         all_dates,
#         key=lambda x: tuple(
#             map(int, x.split("-"))
#         )
#     )
#
#     # --------------------------------------------------------
#     # Create output
#     # --------------------------------------------------------
#
#     with open(
#         output_file,
#         "w",
#         newline="",
#         encoding="utf-8"
#     ) as file:
#
#         writer = csv.writer(file)
#
#         # Header
#         writer.writerow([
#             "Date",
#             "Type",
#             "Price"
#         ])
#
#         # ----------------------------------------------------
#         # OPEN THEN CLOSE FOR EACH DATE
#         # ----------------------------------------------------
#
#         for date in sorted_dates:
#
#             # Open
#             if date in open_data:
#
#                 writer.writerow([
#                     date,
#                     "Open",
#                     open_data[date]
#                 ])
#
#             # Close
#             if date in close_data:
#
#                 writer.writerow([
#                     date,
#                     "Close",
#                     close_data[date]
#                 ])
#
#     print("----------------------------------------")
#     print(f"Created: {output_file}")
#     print(f"Dates processed: {len(sorted_dates):,}")
#     print("----------------------------------------")
#
#
# # ============================================================
# # GOLD BEES
# # ============================================================
#
# create_stacked_file(
#     GOLD_OPEN_FILE,
#     GOLD_CLOSE_FILE,
#     GOLD_OUTPUT
# )
#
#
# # ============================================================
# # SILVER BEES
# # ============================================================
#
# create_stacked_file(
#     SILVER_OPEN_FILE,
#     SILVER_CLOSE_FILE,
#     SILVER_OUTPUT
# )
#
#
# print("Finished successfully.")


import pandas as pd
import os


# ============================================================
# FILE PATHS
# ============================================================

FOLDER = r"D:\prdp\Data Science\Live-Market"

INPUT_FILE = os.path.join(
    FOLDER,
    "EFT-GOLD-SILVER_Joined.csv"
)

OUTPUT_FILE = os.path.join(
    FOLDER,
    "EFT-GOLD-SILVER_Close.csv"
)


# ============================================================
# READ DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)


# ============================================================
# KEEP ONLY CLOSE DATA
# ============================================================

df_close = df[
    df["Status"].str.lower() == "close"
].copy()


# ============================================================
# KEEP ONLY REQUIRED COLUMNS
# ============================================================

df_close = df_close[
    [
        "Date",
        "EFT-Gold",
        "EFT-Silver"
    ]
]


# ============================================================
# SORT BY DATE
# ============================================================

df_close["Date"] = pd.to_datetime(
    df_close["Date"]
)

df_close = df_close.sort_values(
    "Date"
)


# ============================================================
# FORMAT DATE
# ============================================================

df_close["Date"] = df_close[
    "Date"
].dt.strftime("%d-%m-%Y")


# ============================================================
# SAVE
# ============================================================

df_close.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# RESULT
# ============================================================

print("Close-only file created:")
print(OUTPUT_FILE)

print()
print(df_close.head())