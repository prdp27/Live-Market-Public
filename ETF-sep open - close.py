# import csv
# import os
#
#
# # ============================================================
# # FILE PATHS
# # ============================================================
#
# GOLD_FILE = r"D:\prdp\Data Science\Live-Market\EFT-GOLDBEES_Historical_Daily.csv"
#
# SILVER_FILE = r"D:\prdp\Data Science\Live-Market\EFT-SILVERBEES_Historical_Daily.csv"
#
#
# # ============================================================
# # FUNCTION TO SEPARATE OPEN AND CLOSE
# # ============================================================
#
# def separate_open_close(input_file, name):
#
#     folder = os.path.dirname(input_file)
#
#     # Output files
#     open_file = os.path.join(
#         folder,
#         f"{name}_Open.csv"
#     )
#
#     close_file = os.path.join(
#         folder,
#         f"{name}_Close.csv"
#     )
#
#     # --------------------------------------------------------
#     # READ ORIGINAL FILE
#     # --------------------------------------------------------
#
#     with open(
#         input_file,
#         "r",
#         newline="",
#         encoding="utf-8-sig"
#     ) as file:
#
#         reader = csv.DictReader(file)
#
#         # ----------------------------------------------------
#         # CREATE OPEN AND CLOSE FILES
#         # ----------------------------------------------------
#
#         with open(
#             open_file,
#             "w",
#             newline="",
#             encoding="utf-8"
#         ) as open_f, open(
#             close_file,
#             "w",
#             newline="",
#             encoding="utf-8"
#         ) as close_f:
#
#             open_writer = csv.writer(open_f)
#             close_writer = csv.writer(close_f)
#
#             # Headers
#             open_writer.writerow([
#                 "Date",
#                 "Open"
#             ])
#
#             close_writer.writerow([
#                 "Date",
#                 "Close"
#             ])
#
#             # ------------------------------------------------
#             # PROCESS EACH ROW
#             # ------------------------------------------------
#
#             count = 0
#
#             for row in reader:
#
#                 date = row["Date"]
#                 open_price = row["Open"]
#                 close_price = row["Close"]
#
#                 # Write Open
#                 if open_price not in ("", None):
#
#                     open_writer.writerow([
#                         date,
#                         open_price
#                     ])
#
#                 # Write Close
#                 if close_price not in ("", None):
#
#                     close_writer.writerow([
#                         date,
#                         close_price
#                     ])
#
#                 count += 1
#
#     print("----------------------------------------")
#     print(f"Processed : {name}")
#     print(f"Records   : {count:,}")
#     print(f"Open file : {open_file}")
#     print(f"Close file: {close_file}")
#
#
# # ============================================================
# # GOLD BEES
# # ============================================================
#
# separate_open_close(
#     GOLD_FILE,
#     "EFT-GOLDBEES"
# )
#
#
# # ============================================================
# # SILVER BEES
# # ============================================================
#
# separate_open_close(
#     SILVER_FILE,
#     "EFT-SILVERBEES"
# )
#
#
# # ============================================================
# # DONE
# # ============================================================
#
# print("----------------------------------------")
# print("All files created successfully.")



