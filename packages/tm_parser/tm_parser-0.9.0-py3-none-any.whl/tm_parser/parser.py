from .pdf import parse_file
from .output import dump_string, dump_file
from .config import Config


class Parser:
    def __init__(self, config=Config, infile=None, outfile=None, file_format=None):
        self.config = Config
        if infile:
            self.input_file = infile
        if outfile:
            self.output_file = outfile
        if file_format:
            self.output_format = file_format
        self.raw_scouts = []
        self.scouts = parse_file(self.input_file)

    def __len__(self):
        return len(self.scouts)

    def __iter__(self):
        for scout, data in self.scouts.items():
            yield scout, data

    def __str__(self):
        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        return dump_string(self.scouts, self.output_format)

    def dump(self):
        file = self.output_file
        filetype = self.output_format
        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        with open(file, "w", encoding="utf-8") as f:
            dump_file(self.scouts, filetype, outfile=f)

    def dumps(self):
        text_format = self.output_format
        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        return dump_string(self.scouts, text_format)
