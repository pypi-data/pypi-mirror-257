import os
from dotenv import dotenv_values
import toml

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

config = toml.load(os.path.join(basedir, "config.toml"))


class Config:
    # the troop directory is data/TROOP/
    LOG_DIR = TROOP_DIR = os.path.join(basedir, f"data")

    OUTPUT_FORMAT = config.get("OUTPUT_FORMAT", "yaml")
    OUTPUT_TO_FILE = config.get("OUTPUT_TO_FILE", False)

    FILES = {
        "input_file": config.get("INPUT_FILE", os.path.join(TROOP_DIR, "tm_data.pdf")),
        "output_file": config.get(
            "OUTPUT_FILE", os.path.join(TROOP_DIR, f"output.{OUTPUT_FORMAT}")
        ),
    }

    PARTIAL_MB_HEADERS = config.get("PARTIAL_MB_HEADERS")
    OA_HEADERS = config.get("OA_HEADERS")
    ACTIVITY_HEADERS = config.get("ACTIVITY_HEADERS")
    SECTION_MARKERS = config.get("SECTION_MARKERS")
    text_fields = config.get("text_fields")
    date_fields = config.get("date_fields")
    RANKS = config.get("RANKS")
    UPPER_RANKS = config.get("UPPER_RANKS")
    Star = config.get("Star")
    Life = config.get("Life")
    Eagle = config.get("Eagle")
    OUTPUT_RANKS = config.get("OUTPUT_RANKS")
    CSV_HEADER = config.get("CSV_HEADER")

    # coordinates for entire PDF
    WHOLE_PAGE = [0, 0, 612, 792]
    with open(os.path.join(TROOP_DIR, "mb_names.txt"), encoding="utf-8") as f:
        MB_NAMES = [item.strip() for item in f.readlines()]
