import re
from datetime import date

from services.country_service import COUNTRY_NAMES
from services.date_service import parse_date


def is_valid_date(value: str) -> bool:
    return not value or parse_date(value) is not None


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def get_text(form, field_name: str) -> str:
    value = form.get(field_name, "")
    return value.strip() if isinstance(value, str) else ""


def has_valid_phone_length(value: str) -> bool:
    digit_count = len(only_digits(value))
    return 7 <= digit_count <= 15


def validate_w7_form(form) -> list[str]:
    errors = []

    required_fields = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "mailing_street": "Mailing Street Address",
        "mailing_city": "Mailing City / Town",
        "mailing_country": "Mailing Country",
        "date_of_birth": "Date of Birth",
        "country_of_birth": "Country of Birth",
        "birth_city_state": "Birth City and State / Province",
        "citizenship": "Country / Countries of Citizenship",
        "document_issued_by": "Document Issued By",
        "document_number": "Document Number",
        "document_expiration_date": "Document Expiration Date",
        "phone_number": "Phone Number",
    }

    for field_name, label in required_fields.items():
        if not get_text(form, field_name):
            errors.append(f"{label} is required.")

    structured_foreign_address = any(
        get_text(form, field_name)
        for field_name in {
            "foreign_street",
            "foreign_city",
            "foreign_state_province",
            "foreign_country",
            "foreign_postal_code",
        }
    )

    if structured_foreign_address:
        foreign_required_fields = {
            "foreign_street": "Foreign Street Address",
            "foreign_city": "Foreign City / Town",
            "foreign_country": "Foreign Address Country",
        }

        for field_name, label in foreign_required_fields.items():
            if not get_text(form, field_name):
                errors.append(f"{label} is required when a foreign address is entered.")

    country_fields = {
        "Mailing Country": get_text(form, "mailing_country"),
        "Foreign Address Country": get_text(form, "foreign_country"),
        "Country of Birth": get_text(form, "country_of_birth"),
        "Treaty Country": get_text(form, "treaty_country"),
    }

    for label, value in country_fields.items():
        if value and value not in COUNTRY_NAMES:
            errors.append(f"{label} must be selected from the country list.")

    citizenships = [
        country.strip()
        for country in get_text(form, "citizenship").split(";")
        if country.strip()
    ]

    if any(country not in COUNTRY_NAMES for country in citizenships):
        errors.append("Citizenship countries must be selected from the country list.")

    application_type = get_text(form, "application_type")
    reason = get_text(form, "reason")
    reason_f_exception = get_text(form, "reason_f_exception")

    if application_type not in {"new", "renew"}:
        errors.append("Invalid application type.")

    if reason not in set("abcdefgh"):
        errors.append("Invalid application reason.")

    if reason_f_exception not in {"", "yes"}:
        errors.append("Invalid reason f exception selection.")

    if reason != "f" and reason_f_exception:
        errors.append("The reason f exception option can only be used with reason f.")

    if reason == "d":
        if not get_text(form, "reason_d_relationship"):
            errors.append(
                "Relationship is required for reason d."
            )

    if reason in {"d", "e"}:
        if not get_text(form, "reason_e_name"):
            errors.append(
                "Name is required for reason d or e."
            )

        reason_ssn_itin = get_text(form, "reason_e_ssn_itin")

        if not reason_ssn_itin:
            errors.append(
                "SSN / ITIN is required for reason d or e."
            )
        elif len(only_digits(reason_ssn_itin)) != 9:
            errors.append("Reason d/e SSN / ITIN must contain exactly 9 digits.")

    reason_h_required = reason in {"a", "h"} or (
        reason == "f" and reason_f_exception == "yes"
    )

    if reason_h_required:
        if not get_text(form, "reason_h_details"):
            errors.append(
                "Reason h exception details are required."
            )

    if reason in {"a", "f"}:
        if not get_text(form, "treaty_country"):
            errors.append("Treaty Country is required for reason a or f.")

        if not get_text(form, "treaty_article"):
            errors.append("Treaty Article Number is required for reason a or f.")

    if reason == "f":
        institution_fields = {
            "institution_name": "Institution Name",
            "institution_city_state": "Institution City and State",
            "length_of_stay": "Length of Stay",
        }

        for field_name, label in institution_fields.items():
            if not get_text(form, field_name):
                errors.append(f"{label} is required for reason f.")

    gender = get_text(form, "gender")

    if gender not in {"male", "female"}:
        errors.append("Gender is required.")

    document_type = get_text(form, "document_type")

    if document_type not in {"passport", "driver_license", "uscis", "other"}:
        errors.append("Invalid document type.")

    if document_type == "other":
        if not get_text(form, "document_other_description"):
            errors.append(
                "Other document description is required."
            )

    previous_status = get_text(form, "previous_itin_status")

    if previous_status not in {"yes", "no"}:
        errors.append("Previous ITIN / IRSN status is required.")

    itin_value = get_text(form, "itin")
    irsn_value = get_text(form, "irsn")
    itin = only_digits(itin_value)
    irsn = only_digits(irsn_value)

    if previous_status == "yes":
        if not itin and not irsn:
            errors.append(
                "Enter either an ITIN or IRSN."
            )

    if application_type == "renew":
        if previous_status != "yes":
            errors.append("Previous ITIN / IRSN status must be Yes for a renewal.")

        if not itin:
            errors.append("An existing ITIN is required for a renewal.")

    if itin_value and len(itin) != 9:
        errors.append("ITIN must contain exactly 9 digits.")

    if irsn_value and len(irsn) != 9:
        errors.append("IRSN must contain exactly 9 digits.")

    delegate_name = get_text(form, "delegate_name")
    delegate_relationship = get_text(form, "delegate_relationship")

    if delegate_relationship and delegate_relationship not in {
        "parent",
        "power_of_attorney",
        "court_guardian",
    }:
        errors.append("Invalid delegate relationship.")

    if delegate_name and not delegate_relationship:
        errors.append("Delegate Relationship is required when a delegate is named.")

    if delegate_relationship and not delegate_name:
        errors.append("Name of Delegate is required when a relationship is selected.")

    date_fields = {
        "Date of Birth": get_text(form, "date_of_birth"),
        "Visa Expiration Date": get_text(form, "visa_expiration_date"),
        "Document Expiration Date": get_text(form, "document_expiration_date"),
        "U.S. Entry Date": get_text(form, "us_entry_date"),
    }

    for label, value in date_fields.items():
        if value and not is_valid_date(value):
            errors.append(
                f"{label} has an invalid date format."
            )

    date_of_birth = get_text(form, "date_of_birth")

    parsed_birth_date = parse_date(date_of_birth)

    if parsed_birth_date:
        if parsed_birth_date.date() > date.today():
            errors.append("Date of Birth cannot be in the future.")

    phone_fields = {
        "Phone Number": get_text(form, "phone_number"),
        "Acceptance Agent Phone": get_text(form, "agent_phone"),
        "Acceptance Agent Fax": get_text(form, "agent_fax"),
    }

    for label, value in phone_fields.items():
        if value and not has_valid_phone_length(value):
            errors.append(f"{label} must contain between 7 and 15 digits.")

    agent_ein = get_text(form, "agent_ein")

    if agent_ein and len(only_digits(agent_ein)) != 9:
        errors.append("Acceptance Agent EIN must contain exactly 9 digits.")

    agent_ptin = get_text(form, "agent_ptin").upper()

    if agent_ptin and not re.fullmatch(r"P\d{8}", agent_ptin):
        errors.append("Acceptance Agent PTIN must use the format P12345678.")

    return errors
