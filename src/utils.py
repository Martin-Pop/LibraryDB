import re

class InvalidParameterException(Exception):
    pass

class DatabaseConnectionException(Exception):
    pass

def parse_db_exception(exception):
    msg = str(exception)

    if 'UNIQUE' in msg:
        pattern = r"The duplicate key value is \((.*?)\)\."
        match = re.search(pattern, msg)
        if match:
            return f"{match.group(1)} isn't unique"
        return "unique value violation"
    elif 'REFERENCE' in msg:
        return "please remove all references before proceeding"
    else:
        return msg