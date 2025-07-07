def validate_int(value):
    if not value.strip().isdigit():
        raise ValueError("Invalid integer input.")
    return int(value.strip())

def validate_boolean(value):
    value = value.strip()
    if value not in ['0', '1']:
        raise ValueError("Only 0 (False) or 1 (True) allowed.")
    return bool(int(value))

def validate_date(value):
    from datetime import datetime
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")
