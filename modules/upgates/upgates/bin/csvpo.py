"""
Convert between PO and CSV files.
"""

import csv
import sys
from pathlib import Path

import polib

DATA_PATH = Path("~/.neven/data")

VALID_LANGS = ("English", "Czech", "Slovak")


def po2csv(po_file, lang: str):
    """Convert po to csv."""
    po = polib.pofile(po_file)

    if lang not in VALID_LANGS:
        raise ValueError(f"Invalid Language: {lang}")

    output_file = f"messages-{lang.lower()}.csv"

    with open(output_file, "w", encoding="utf8") as csvfile:
        csvfile.writelines([f"[MESSAGE_ID], [{lang}]\n"])

        for entry in po:
            msgid = entry.msgid.replace('"', "'")
            msgstr = entry.msgstr.replace('"', "'")

            line = f'"{msgid}", "{msgstr}"\n'
            csvfile.writelines([line])


def csv2po(csv_file: Path, output_path: Path) -> None:
    """Convert csv to po."""
    po = polib.POFile()

    with open(csv_file, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                continue  ## skip the header row
            entry = polib.POEntry(msgid=row[0], msgstr=row[1])
            po.append(entry)

    po.save(output_path.as_posix())

    return None


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <po2csv|csv2po> <input_file> <language:'English'>")
        sys.exit(1)

    command = sys.argv[1]
    input_path = Path(sys.argv[2]).expanduser()

    if command == "po2csv":
        language = sys.argv[3] if len(sys.argv) >= 4 else ""
        po2csv(input_path, language)
    elif command == "csv2po":
        output_path = Path(sys.argv[3] if len(sys.argv) >= 4 else "out.po").expanduser()
        csv2po(input_path, output_path)
        print(f"Saved: {output_path}")
    else:
        print(f"Invvalid command: {command}")


if __name__ == "__main__":
    main()
