from datetime import datetime
from pathlib import Path
import re

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject

from mappings.w7_2024 import W7_FIELDS, W7_CHECKBOX_VALUES


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "fw7.pdf"



def normalize_date(value: str) -> str:
    """
    Web formundan veya manuel girişten gelen tarihi
    IRS PDF'nin beklediği MMDDYYYY formatına dönüştürür.

    Desteklenen örnekler:
    1995-06-15
    06/15/1995
    06-15-1995
    """
    if not value:
        return ""

    value = value.strip()

    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
    ]

    for date_format in formats:
        try:
            parsed = datetime.strptime(value, date_format)
            return parsed.strftime("%m%d%Y")
        except ValueError:
            continue

    raise ValueError(
        "Geçersiz tarih formatı. "
        "YYYY-MM-DD veya MM/DD/YYYY kullanın."
    )


def split_itin(value: str):
    """
    ITIN formatını üç parçaya ayırır.

    Örnek:
    912-34-5678
       ↓
    912 | 34 | 5678
    """
    if not value:
        return "", "", ""

    digits = re.sub(r"\D", "", value)

    if len(digits) != 9:
        raise ValueError("ITIN 9 haneli olmalıdır.")

    return digits[:3], digits[3:5], digits[5:]


def split_irsn(value: str):
    """
    IRSN için de aynı 9 haneli parçalama mantığını kullanır.
    """
    if not value:
        return "", "", ""

    digits = re.sub(r"\D", "", value)

    if len(digits) != 9:
        raise ValueError("IRSN 9 haneli olmalıdır.")

    return digits[:3], digits[3:5], digits[5:]


def set_text(form_data: dict, logical_name: str, value: str):
    """
    Boş olmayan text değerini ilgili PDF alanına ekler.
    """
    if value not in (None, ""):
        form_data[W7_FIELDS[logical_name]] = str(value)


def set_checkbox(form_data: dict, logical_name: str):
    """
    Checkbox'ın doğru export değerini form_data'ya ekler.
    """
    form_data[W7_FIELDS[logical_name]] = W7_CHECKBOX_VALUES[logical_name]


def generate_w7(
    output_path,

    # Application
    application_type,
    reason,
    include_reason_h=False,

    reason_d_relationship="",
    reason_e_name="",
    reason_e_ssn_itin="",
    reason_h_details="",
    treaty_country="",
    treaty_article="",

    # Name
    first_name="",
    middle_name="",
    last_name="",
    birth_first_name="",
    birth_middle_name="",
    birth_last_name="",

    # Mailing address
    mailing_street="",
    mailing_city_country_postal="",

    # Foreign address
    foreign_street="",
    foreign_city_country_postal="",

    # Birth
    date_of_birth="",
    country_of_birth="",
    birth_city_state="",
    gender="",

    # Other information
    citizenship="",
    foreign_tax_id="",
    us_visa="",

    # Identification
    document_type="",
    document_other_description="",
    document_issued_by="",
    document_number="",
    document_expiration_date="",
    us_entry_date="",

    # Previous ITIN / IRSN
    previous_itin_status="",
    itin="",
    irsn="",
    previous_first_name="",
    previous_middle_name="",
    previous_last_name="",

    # Institution
    institution_name="",
    institution_city_state="",
    length_of_stay="",

    # Sign / delegate
    phone_number="",
    delegate_name="",
    delegate_relationship="",

    # Acceptance Agent
    agent_phone="",
    agent_fax="",
    agent_name_title="",
    agent_company="",
    agent_ein="",
    agent_ptin="",
    agent_office_code="",
):
    reader = PdfReader(str(TEMPLATE_PATH))
    writer = PdfWriter()

    writer.clone_document_from_reader(reader)

    acroform_ref = writer._root_object.get("/AcroForm")

    if acroform_ref:
        acroform = acroform_ref.get_object()
        acroform[NameObject("/NeedAppearances")] = BooleanObject(True)

    form_data = {}

    # ==================================================
    # APPLICATION TYPE
    # ==================================================

    if application_type == "new":
        set_checkbox(form_data, "apply_new_itin")

    elif application_type == "renew":
        set_checkbox(form_data, "renew_itin")

    else:
        raise ValueError("application_type 'new' veya 'renew' olmalıdır.")

    # ==================================================
    # REASON
    # ==================================================

    reason = reason.lower().strip()
    reason_key = f"reason_{reason}"

    if reason_key not in W7_FIELDS:
        raise ValueError("Reason a ile h arasında olmalıdır.")

    set_checkbox(form_data, reason_key)

    reason_h_selected = reason in {"a", "h"} or (
        reason == "f" and include_reason_h
    )

    if reason_h_selected and reason != "h":
        set_checkbox(form_data, "reason_h")

    if reason == "d":
        set_text(
            form_data,
            "reason_d_relationship",
            reason_d_relationship,
        )

    if reason in {"d", "e"}:
        set_text(form_data, "reason_e_name", reason_e_name)
        set_text(form_data, "reason_e_ssn_itin", reason_e_ssn_itin)

    if reason_h_selected:
        set_text(form_data, "reason_h_details", reason_h_details)

    if reason in {"a", "f"}:
        set_text(form_data, "treaty_country", treaty_country)
        set_text(form_data, "treaty_article", treaty_article)

    # ==================================================
    # NAME
    # ==================================================

    set_text(form_data, "first_name", first_name)
    set_text(form_data, "middle_name", middle_name)
    set_text(form_data, "last_name", last_name)

    set_text(form_data, "birth_first_name", birth_first_name)
    set_text(form_data, "birth_middle_name", birth_middle_name)
    set_text(form_data, "birth_last_name", birth_last_name)

    # ==================================================
    # ADDRESSES
    # ==================================================

    set_text(form_data, "mailing_street", mailing_street)

    set_text(
        form_data,
        "mailing_city_country_postal",
        mailing_city_country_postal,
    )

    set_text(form_data, "foreign_street", foreign_street)

    set_text(
        form_data,
        "foreign_city_country_postal",
        foreign_city_country_postal,
    )

    # ==================================================
    # BIRTH INFORMATION
    # ==================================================

    if date_of_birth:
        set_text(
            form_data,
            "date_of_birth",
            normalize_date(date_of_birth),
        )

    set_text(form_data, "country_of_birth", country_of_birth)
    set_text(form_data, "birth_city_state", birth_city_state)

    if gender == "male":
        set_checkbox(form_data, "gender_male")

    elif gender == "female":
        set_checkbox(form_data, "gender_female")

    # ==================================================
    # OTHER INFORMATION
    # ==================================================

    set_text(form_data, "citizenship", citizenship)
    set_text(form_data, "foreign_tax_id", foreign_tax_id)
    set_text(form_data, "us_visa", us_visa)

    # ==================================================
    # IDENTIFICATION DOCUMENT
    # ==================================================

    document_map = {
        "passport": "document_passport",
        "driver_license": "document_driver_license",
        "uscis": "document_uscis",
        "other": "document_other",
    }

    if document_type in document_map:
        set_checkbox(form_data, document_map[document_type])

    set_text(
        form_data,
        "document_other_description",
        document_other_description,
    )

    set_text(
        form_data,
        "document_issued_by",
        document_issued_by,
    )

    set_text(
        form_data,
        "document_number",
        document_number,
    )

    if document_expiration_date:
        set_text(
            form_data,
            "document_expiration_date",
            normalize_date(document_expiration_date),
        )

    if us_entry_date:
        set_text(
            form_data,
            "us_entry_date",
            normalize_date(us_entry_date),
        )

    # ==================================================
    # PREVIOUS ITIN / IRSN
    # ==================================================

    if previous_itin_status == "no":
        set_checkbox(form_data, "previous_itin_no")

    elif previous_itin_status == "yes":
        set_checkbox(form_data, "previous_itin_yes")

    if itin:
        itin_1, itin_2, itin_3 = split_itin(itin)

        set_text(form_data, "itin_part_1", itin_1)
        set_text(form_data, "itin_part_2", itin_2)
        set_text(form_data, "itin_part_3", itin_3)

    if irsn:
        irsn_1, irsn_2, irsn_3 = split_irsn(irsn)

        set_text(form_data, "irsn_part_1", irsn_1)
        set_text(form_data, "irsn_part_2", irsn_2)
        set_text(form_data, "irsn_part_3", irsn_3)

    set_text(
        form_data,
        "previous_first_name",
        previous_first_name,
    )

    set_text(
        form_data,
        "previous_middle_name",
        previous_middle_name,
    )

    set_text(
        form_data,
        "previous_last_name",
        previous_last_name,
    )

    # ==================================================
    # INSTITUTION
    # ==================================================

    set_text(form_data, "institution_name", institution_name)

    set_text(
        form_data,
        "institution_city_state",
        institution_city_state,
    )

    set_text(form_data, "length_of_stay", length_of_stay)

    # ==================================================
    # SIGN / DELEGATE
    # ==================================================

    set_text(form_data, "phone_number", phone_number)
    set_text(form_data, "delegate_name", delegate_name)

    delegate_map = {
        "parent": "delegate_parent",
        "power_of_attorney": "delegate_power_of_attorney",
        "court_guardian": "delegate_court_guardian",
    }

    if delegate_relationship in delegate_map:
        set_checkbox(
            form_data,
            delegate_map[delegate_relationship],
        )

    # ==================================================
    # ACCEPTANCE AGENT
    # ==================================================

    set_text(form_data, "agent_phone", agent_phone)
    set_text(form_data, "agent_fax", agent_fax)
    set_text(form_data, "agent_name_title", agent_name_title)
    set_text(form_data, "agent_company", agent_company)
    set_text(form_data, "agent_ein", agent_ein)
    set_text(form_data, "agent_ptin", agent_ptin)
    set_text(form_data, "agent_office_code", agent_office_code)

    # ==================================================
    # WRITE PDF
    # ==================================================

    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            form_data,
            auto_regenerate=False,
        )

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return output_path
