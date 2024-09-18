from datetime import datetime

def try_strptime(s, formats):
    for format in formats:
        try:
            return datetime.strptime(s, format)
        except ValueError:
            pass
    raise ValueError(f"Time {s} does not match any of the formats.")