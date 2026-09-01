import csv
import os


# ============================================================
# SETTINGS
# ============================================================

FOLDER = r"D:\prdp\Data Science\Live-Market"

MAIN_FILE = os.path.join(
    FOLDER,
    "Live-Market.csv"
)

ETF_FILE = os.path.join(
    FOLDER,
    "EFT-GOLD-SILVER_Close.csv"
)

OUTPUT_FILE = os.path.join(
    FOLDER,
    "Correction-new.csv"
)


# ============================================================
# READ ETF CLOSE DATA
# ============================================================

etf_data = {}

with open(
    ETF_FILE,
    "r",
    newline="",
    encoding="utf-8-sig"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        date = row["Date"].strip()

        gold = row["EFT-Gold"].strip()
        silver = row["EFT-Silver"].strip()

        # ----------------------------------------------------
        # Format ONLY ETF values
        # ----------------------------------------------------

        if gold:
            try:
                gold = f"{float(gold):.6f}"
            except ValueError:
                pass

        if silver:
            try:
                silver = f"{float(silver):.6f}"
            except ValueError:
                pass

        etf_data[date] = (
            gold,
            silver
        )


# ============================================================
# READ MAIN FILE
# ============================================================

with open(
    MAIN_FILE,
    "r",
    newline="",
    encoding="utf-8-sig"
) as source:

    reader = csv.reader(source)

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header = next(reader)

    # --------------------------------------------------------
    # FIND COLUMN POSITIONS
    # --------------------------------------------------------

    date_index = header.index("DMD-Date")
    gold_index = header.index("ETF-Gold")
    silver_index = header.index("ETF-Silver")


    # ========================================================
    # OUTPUT FILE
    # ========================================================

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as destination:

        writer = csv.writer(
            destination,
            lineterminator="\n"
        )

        # ----------------------------------------------------
        # WRITE ORIGINAL HEADER
        # ----------------------------------------------------

        writer.writerow(header)


        # ----------------------------------------------------
        # PROCESS ROWS
        # ----------------------------------------------------

        row_count = 0
        matched_count = 0
        short_rows = 0

        for row in reader:

            row_count += 1

            # ------------------------------------------------
            # CHECK ROW LENGTH
            # ------------------------------------------------
            #
            # If a row has fewer columns than the header,
            # add blank fields so the row is valid.
            #
            # Existing values are NOT changed.
            # ------------------------------------------------

            if len(row) < len(header):

                short_rows += 1

                row.extend(
                    [""] * (
                        len(header) - len(row)
                    )
                )

            # ------------------------------------------------
            # DATE
            # ------------------------------------------------

            date = row[date_index].strip()

            # ------------------------------------------------
            # FIND ETF DATA
            # ------------------------------------------------

            if date in etf_data:

                gold, silver = etf_data[date]

                # --------------------------------------------
                # Replace ONLY ETF-Gold
                # --------------------------------------------

                if gold:
                    row[gold_index] = gold

                # --------------------------------------------
                # Replace ONLY ETF-Silver
                # --------------------------------------------

                if silver:
                    row[silver_index] = silver

                matched_count += 1

            # ------------------------------------------------
            # WRITE ROW
            # ------------------------------------------------

            writer.writerow(row)


# ============================================================
# RESULT
# ============================================================

print()
print("============================================")
print("CORRECTION FILE CREATED")
print("============================================")

print(
    f"Original rows : {row_count:,}"
)

print(
    f"ETF matched   : {matched_count:,}"
)

print(
    f"Short rows    : {short_rows:,}"
)

print()
print(
    "Output:"
)

print(
    OUTPUT_FILE
)

print("============================================")



# ===================================
# import csv
# import os
#
#
# # ============================================================
# # FILE PATHS
# # ============================================================
#
# FOLDER = r"D:\prdp\Data Science\Live-Market"
#
# MAIN_FILE = os.path.join(
#     FOLDER,
#     "Live-Market.csv"
# )
#
# ETF_FILE = os.path.join(
#     FOLDER,
#     "EFT-GOLD-SILVER_Close.csv"
# )
#
# OUTPUT_FILE = os.path.join(
#     FOLDER,
#     "Correction.csv"
# )
#
#
# # ============================================================
# # READ ETF CLOSE DATA
# # ============================================================
#
# etf_data = {}
#
# with open(
#     ETF_FILE,
#     "r",
#     newline="",
#     encoding="utf-8-sig"
# ) as f:
#
#     reader = csv.DictReader(f)
#
#     for row in reader:
#
#         date = row["Date"].strip()
#
#         gold = row["EFT-Gold"].strip()
#         silver = row["EFT-Silver"].strip()
#
#         etf_data[date] = (
#             gold,
#             silver
#         )
#
#
# # ============================================================
# # READ MAIN FILE WITHOUT CHANGING ANY EXISTING DATA
# # ============================================================
#
# with open(
#     MAIN_FILE,
#     "r",
#     newline="",
#     encoding="utf-8-sig"
# ) as f:
#
#     reader = csv.DictReader(f)
#
#     existing_headers = reader.fieldnames
#
#     rows = list(reader)
#
#
# # ============================================================
# # NEW COLUMN NAMES
# # ============================================================
# #
# # These are NEW columns.
# # Existing columns/data are NOT touched.
# #
# # ============================================================
#
# gold_column = "ETF-Gold-New"
# silver_column = "ETF-Silver-New"
#
#
# # Add only the new columns
#
# new_headers = existing_headers + [
#     gold_column,
#     silver_column
# ]
#
#
# # ============================================================
# # CREATE CORRECTION.CSV
# # ============================================================
#
# with open(
#     OUTPUT_FILE,
#     "w",
#     newline="",
#     encoding="utf-8"
# ) as f:
#
#     writer = csv.DictWriter(
#         f,
#         fieldnames=new_headers
#     )
#
#     # Header
#     writer.writeheader()
#
#     # --------------------------------------------------------
#     # EXISTING ROWS
#     # --------------------------------------------------------
#
#     for row in rows:
#
#         # Keep existing data EXACTLY as read
#         date = row["DMD-Date"].strip()
#
#         # Get ETF data for this date
#         gold, silver = etf_data.get(
#             date,
#             ("", "")
#         )
#
#         # ----------------------------------------------------
#         # ONLY FORMAT THE NEW ETF DATA
#         # ----------------------------------------------------
#
#         if gold != "":
#             try:
#                 gold = f"{float(gold):.6f}"
#             except ValueError:
#                 pass
#
#         if silver != "":
#             try:
#                 silver = f"{float(silver):.6f}"
#             except ValueError:
#                 pass
#
#         # Add ONLY new values
#         row[gold_column] = gold
#         row[silver_column] = silver
#
#         # Write row
#         writer.writerow(row)
#
#
# # ============================================================
# # COMPLETE
# # ============================================================
#
# print("============================================")
# print("Correction.csv created")
# print("============================================")
#
# print(
#     f"Original rows : {len(rows):,}"
# )
#
# print(
#     f"ETF dates     : {len(etf_data):,}"
# )
#
# print(
#     f"Output file   : {OUTPUT_FILE}"
# )
#
# print("============================================")
#
#
#
# # import csv
#
# # import os
# # from datetime import datetime
# #
# #
# # # ============================================================
# # # FILE PATHS
# # # ============================================================
# #
# # FOLDER = r"D:\prdp\Data Science\Live-Market"
# #
# # GOLD_FILE = os.path.join(
# #     FOLDER,
# #     "EFT-GOLDBEES_Stacked.csv"
# # )
# #
# # SILVER_FILE = os.path.join(
# #     FOLDER,
# #     "EFT-SILVERBEES_Stacked.csv"
# # )
# #
# # OUTPUT_FILE = os.path.join(
# #     FOLDER,
# #     "EFT-GOLD-SILVER_Joined.csv"
# # )
# #
# #
# # # ============================================================
# # # READ STACKED FILE
# # # ============================================================
# #
# # def read_stacked_file(file_path):
# #
# #     data = {}
# #
# #     with open(
# #         file_path,
# #         "r",
# #         newline="",
# #         encoding="utf-8-sig"
# #     ) as file:
# #
# #         reader = csv.DictReader(file)
# #
# #         for row in reader:
# #
# #             date = row["Date"].strip()
# #             status = row["Type"].strip().lower()
# #             price = row["Price"].strip()
# #
# #             # Key = Date + Status
# #             key = (date, status)
# #
# #             data[key] = price
# #
# #     return data
# #
# #
# # # ============================================================
# # # READ GOLD
# # # ============================================================
# #
# # print("Reading Gold...")
# #
# # gold_data = read_stacked_file(
# #     GOLD_FILE
# # )
# #
# #
# # # ============================================================
# # # READ SILVER
# # # ============================================================
# #
# # print("Reading Silver...")
# #
# # silver_data = read_stacked_file(
# #     SILVER_FILE
# # )
# #
# #
# # # ============================================================
# # # CREATE ALL DATE + STATUS KEYS
# # # ============================================================
# #
# # all_keys = set()
# #
# # all_keys.update(
# #     gold_data.keys()
# # )
# #
# # all_keys.update(
# #     silver_data.keys()
# # )
# #
# #
# # # ============================================================
# # # SORT BY DATE THEN STATUS
# # # OPEN FIRST, CLOSE SECOND
# # # ============================================================
# #
# # def sort_key(key):
# #
# #     date, status = key
# #
# #     date_value = datetime.strptime(
# #         date,
# #         "%Y-%m-%d"
# #     )
# #
# #     # Open = 0
# #     # Close = 1
# #
# #     status_order = {
# #         "open": 0,
# #         "close": 1
# #     }
# #
# #     return (
# #         date_value,
# #         status_order.get(
# #             status,
# #             99
# #         )
# #     )
# #
# #
# # sorted_keys = sorted(
# #     all_keys,
# #     key=sort_key
# # )
# #
# #
# # # ============================================================
# # # WRITE JOINED FILE
# # # ============================================================
# #
# # with open(
# #     OUTPUT_FILE,
# #     "w",
# #     newline="",
# #     encoding="utf-8"
# # ) as file:
# #
# #     writer = csv.writer(file)
# #
# #     # --------------------------------------------------------
# #     # HEADER
# #     # --------------------------------------------------------
# #
# #     writer.writerow([
# #         "Date",
# #         "Status",
# #         "EFT-Gold",
# #         "EFT-Silver"
# #     ])
# #
# #     # --------------------------------------------------------
# #     # DATA
# #     # --------------------------------------------------------
# #
# #     for date, status in sorted_keys:
# #
# #         writer.writerow([
# #             date,
# #             status.capitalize(),
# #
# #             # Gold
# #             gold_data.get(
# #                 (date, status),
# #                 ""
# #             ),
# #
# #             # Silver
# #             silver_data.get(
# #                 (date, status),
# #                 ""
# #             )
# #         ])
# #
# #
# # # ============================================================
# # # SUMMARY
# # # ============================================================
# #
# # print()
# # print("============================================")
# # print("JOIN COMPLETE")
# # print("============================================")
# #
# # print(
# #     f"Gold records   : {len(gold_data):,}"
# # )
# #
# # print(
# #     f"Silver records : {len(silver_data):,}"
# # )
# #
# # print(
# #     f"Total rows     : {len(sorted_keys):,}"
# # )
# #
# # print()
# # print(
# #     f"Output file:\n{OUTPUT_FILE}"
# # )
# #
# # print("============================================")
