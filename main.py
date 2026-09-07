from pathlib import Path
import uuid

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from services.country_service import COUNTRIES
from services.pdf_service import generate_w7
from services.validation_service import validate_w7_form


app = FastAPI(
    title="W-7 Document Automation PoC",
    description="IRS Form W-7 document automation prototype",
)

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

GENERATED_DIR = BASE_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)


def combine_address_parts(form: dict, prefix: str, legacy_field: str) -> None:
    parts = [
        form.get(f"{prefix}_city", ""),
        form.get(f"{prefix}_state_province", ""),
        form.get(f"{prefix}_country", ""),
        form.get(f"{prefix}_postal_code", ""),
    ]

    if any(parts):
        form[legacy_field] = ", ".join(part for part in parts if part)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"countries": COUNTRIES}
    )


@app.post("/generate")
async def generate_pdf(request: Request):

    submitted_form = await request.form()
    has_file_upload = any(
        not isinstance(value, str)
        for _, value in submitted_form.multi_items()
    )
    form = {
        key: value.strip()
        for key, value in submitted_form.items()
        if isinstance(value, str)
    }

    citizenship_values = [
        value.strip()
        for value in submitted_form.getlist("citizenship")
        if isinstance(value, str) and value.strip()
    ]

    if citizenship_values:
        form["citizenship"] = "; ".join(dict.fromkeys(citizenship_values))

    combine_address_parts(form, "mailing", "mailing_city_country_postal")
    combine_address_parts(form, "foreign", "foreign_city_country_postal")

    errors = validate_w7_form(form)

    if has_file_upload:
        errors.append("File uploads are not supported.")

    if errors:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "errors": errors,
                "form_data": dict(form),
                "countries": COUNTRIES,
            },
            status_code=400,
        )

    unique_id = uuid.uuid4().hex[:8]

    output_path = GENERATED_DIR / f"w7_{unique_id}.pdf"

    generate_w7(
        output_path=output_path,

        application_type=form.get("application_type", "new"),
        reason=form.get("reason", "b"),
        include_reason_h=form.get("reason_f_exception") == "yes",

        reason_d_relationship=form.get(
            "reason_d_relationship", ""
        ),

        reason_e_name=form.get(
            "reason_e_name", ""
        ),

        reason_e_ssn_itin=form.get(
            "reason_e_ssn_itin", ""
        ),

        reason_h_details=form.get(
            "reason_h_details", ""
        ),

        treaty_country=form.get(
            "treaty_country", ""
        ),

        treaty_article=form.get(
            "treaty_article", ""
        ),

        first_name=form.get("first_name", ""),
        middle_name=form.get("middle_name", ""),
        last_name=form.get("last_name", ""),

        birth_first_name=form.get(
            "birth_first_name", ""
        ),

        birth_middle_name=form.get(
            "birth_middle_name", ""
        ),

        birth_last_name=form.get(
            "birth_last_name", ""
        ),

        mailing_street=form.get(
            "mailing_street", ""
        ),

        mailing_city_country_postal=form.get(
            "mailing_city_country_postal", ""
        ),

        foreign_street=form.get(
            "foreign_street", ""
        ),

        foreign_city_country_postal=form.get(
            "foreign_city_country_postal", ""
        ),

        date_of_birth=form.get(
            "date_of_birth", ""
        ),

        country_of_birth=form.get(
            "country_of_birth", ""
        ),

        birth_city_state=form.get(
            "birth_city_state", ""
        ),

        gender=form.get("gender", ""),

        citizenship=form.get(
            "citizenship", ""
        ),

        foreign_tax_id=form.get(
            "foreign_tax_id", ""
        ),

        visa_type=form.get("visa_type", ""),
        visa_number=form.get("visa_number", ""),
        visa_expiration_date=form.get("visa_expiration_date", ""),

        document_type=form.get(
            "document_type", ""
        ),

        document_other_description=form.get(
            "document_other_description", ""
        ),

        document_issued_by=form.get(
            "document_issued_by", ""
        ),

        document_number=form.get(
            "document_number", ""
        ),

        document_expiration_date=form.get(
            "document_expiration_date", ""
        ),

        us_entry_date=form.get(
            "us_entry_date", ""
        ),

        previous_itin_status=form.get(
            "previous_itin_status", ""
        ),

        itin=form.get("itin", ""),
        irsn=form.get("irsn", ""),

        previous_first_name=form.get(
            "previous_first_name", ""
        ),

        previous_middle_name=form.get(
            "previous_middle_name", ""
        ),

        previous_last_name=form.get(
            "previous_last_name", ""
        ),

        institution_name=form.get(
            "institution_name", ""
        ),

        institution_city_state=form.get(
            "institution_city_state", ""
        ),

        length_of_stay=form.get(
            "length_of_stay", ""
        ),

        phone_number=form.get(
            "phone_number", ""
        ),

        delegate_name=form.get(
            "delegate_name", ""
        ),

        delegate_relationship=form.get(
            "delegate_relationship", ""
        ),

        agent_phone=form.get(
            "agent_phone", ""
        ),

        agent_fax=form.get(
            "agent_fax", ""
        ),

        agent_name_title=form.get(
            "agent_name_title", ""
        ),

        agent_company=form.get(
            "agent_company", ""
        ),

        agent_ein=form.get(
            "agent_ein", ""
        ),

        agent_ptin=form.get(
            "agent_ptin", ""
        ),

        agent_office_code=form.get(
            "agent_office_code", ""
        ),
    )

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename="generated_w7.pdf",
    )
