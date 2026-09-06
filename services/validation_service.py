import re
from datetime import datetime


def is_valid_date(value: str) -> bool:
    if not value:
        return True

    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
    ]

    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            continue

    return False


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_w7_form(form) -> list[str]:
    errors = []

    first_name = form.get("first_name", "").strip()
    last_name = form.get("last_name", "").strip()

    application_type = form.get("application_type", "")
    reason = form.get("reason", "")

    if not first_name:
        errors.append("First Name is required.")

    if not last_name:
        errors.append("Last Name is required.")

    if application_type not in {"new", "renew"}:
        errors.append("Invalid application type.")

    if reason not in set("abcdefgh"):
        errors.append("Invalid application reason.")

    if reason == "d":
        if not form.get("reason_d_relationship", "").strip():
            errors.append(
                "Relationship is required for reason d."
            )

    if reason == "e":
        if not form.get("reason_e_name", "").strip():
            errors.append(
                "Name is required for reason e."
            )

        if not form.get("reason_e_ssn_itin", "").strip():
            errors.append(
                "SSN / ITIN is required for reason e."
            )

    if reason == "h":
        if not form.get("reason_h_details", "").strip():
            errors.append(
                "Other reason details are required for reason h."
            )

    document_type = form.get("document_type", "")

    if document_type == "other":
        if not form.get(
            "document_other_description", ""
        ).strip():
            errors.append(
                "Other document description is required."
            )

    previous_status = form.get(
        "previous_itin_status", ""
    )

    if previous_status == "yes":
        itin = only_digits(form.get("itin", ""))
        irsn = only_digits(form.get("irsn", ""))

        if not itin and not irsn:
            errors.append(
                "Enter either an ITIN or IRSN."
            )

        if itin and len(itin) != 9:
            errors.append(
                "ITIN must contain exactly 9 digits."
            )

        if irsn and len(irsn) != 9:
            errors.append(
                "IRSN must contain exactly 9 digits."
            )

    date_fields = {
        "Date of Birth": form.get(
            "date_of_birth", ""
        ),
        "Document Expiration Date": form.get(
            "document_expiration_date", ""
        ),
        "U.S. Entry Date": form.get(
            "us_entry_date", ""
        ),
        "Acceptance Agent Date": form.get(
            "agent_date", ""
        ),
    }

    for label, value in date_fields.items():
        if value and not is_valid_date(value):
            errors.append(
                f"{label} has an invalid date format."
            )

    return errors