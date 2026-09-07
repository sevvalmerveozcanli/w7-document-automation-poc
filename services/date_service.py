from datetime import datetime


DATE_FORMATS = (
    "%d.%m.%Y",
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m-%d-%Y",
)


def parse_date(value: str) -> datetime | None:
    if not value:
        return None

    value = value.strip()

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def format_date_for_pdf(value: str) -> str:
    if not value:
        return ""

    parsed = parse_date(value)

    if not parsed:
        raise ValueError(
            "Invalid date format. Use DD.MM.YYYY, YYYY-MM-DD, or MM/DD/YYYY."
        )

    return parsed.strftime("%m/%d/%Y")
