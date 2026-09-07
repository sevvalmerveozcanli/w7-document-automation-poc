import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from mappings.w7_2024 import W7_FIELDS
from services.date_service import format_date_for_pdf
from services.pdf_service import generate_w7
from services.validation_service import validate_w7_form


def valid_form() -> dict[str, str]:
    return {
        "application_type": "new",
        "reason": "b",
        "first_name": "Test",
        "last_name": "Applicant",
        "mailing_street": "1 Main Street",
        "mailing_city": "Istanbul",
        "mailing_country": "Turkey",
        "date_of_birth": "27.02.2004",
        "country_of_birth": "Turkey",
        "birth_city_state": "Istanbul",
        "gender": "male",
        "citizenship": "Turkey",
        "document_type": "passport",
        "document_issued_by": "Turkey",
        "document_number": "P123456",
        "document_expiration_date": "12.01.2030",
        "previous_itin_status": "no",
        "phone_number": "+90 555 123 4567",
    }


def generated_field_values(**values) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as directory:
        output_path = Path(directory) / "w7.pdf"
        generate_w7(output_path, application_type="new", reason="b", **values)
        fields = PdfReader(str(output_path)).get_fields()
        return {
            field_name: field.get("/V")
            for field_name, field in fields.items()
        }


def get_pdf_value(fields: dict[str, str], logical_name: str) -> str | None:
    field_suffix = W7_FIELDS[logical_name]
    return next(
        value
        for field_name, value in fields.items()
        if field_name.endswith(field_suffix)
    )


class W7ChangeTests(unittest.TestCase):
    def test_a_visa_information_can_be_completely_empty(self):
        self.assertEqual(validate_w7_form(valid_form()), [])

        fields = generated_field_values()
        self.assertFalse(get_pdf_value(fields, "us_visa"))

    def test_b_visa_information_is_joined_without_extra_commas(self):
        fields = generated_field_values(
            visa_type="B1/B2",
            visa_number="ABC123456",
            visa_expiration_date="12.01.2030",
        )

        self.assertEqual(
            get_pdf_value(fields, "us_visa"),
            "B1/B2, ABC123456, 01/12/2030",
        )

        number_only_fields = generated_field_values(visa_number="ABC123456")
        self.assertEqual(get_pdf_value(number_only_fields, "us_visa"), "ABC123456")

    def test_c_foreign_city_is_required_for_entered_address(self):
        form = valid_form()
        form.update({"foreign_street": "2 Side Street", "foreign_country": "Turkey"})

        self.assertIn(
            "Foreign City / Town is required when a foreign address is entered.",
            validate_w7_form(form),
        )

    def test_d_foreign_country_is_required_for_entered_address(self):
        form = valid_form()
        form.update({"foreign_street": "2 Side Street", "foreign_city": "Ankara"})

        self.assertIn(
            "Foreign Address Country is required when a foreign address is entered.",
            validate_w7_form(form),
        )

    def test_foreign_street_is_required_but_state_and_postal_are_optional(self):
        form = valid_form()
        form.update({
            "foreign_city": "Ankara",
            "foreign_country": "Turkey",
        })

        self.assertIn(
            "Foreign Street Address is required when a foreign address is entered.",
            validate_w7_form(form),
        )

        form["foreign_street"] = "2 Side Street"
        self.assertEqual(validate_w7_form(form), [])

    def test_mailing_city_and_country_are_required_but_postal_is_optional(self):
        form = valid_form()
        self.assertEqual(validate_w7_form(form), [])

        form.pop("mailing_city")
        form.pop("mailing_country")
        errors = validate_w7_form(form)
        self.assertIn("Mailing City / Town is required.", errors)
        self.assertIn("Mailing Country is required.", errors)

    def test_e_turkish_birth_date_is_formatted_for_pdf(self):
        fields = generated_field_values(date_of_birth="27.02.2004")

        self.assertEqual(get_pdf_value(fields, "date_of_birth"), "02/27/2004")

    def test_f_turkish_expiration_date_is_formatted_for_pdf(self):
        self.assertEqual(format_date_for_pdf("12.01.2030"), "01/12/2030")

        fields = generated_field_values(
            document_expiration_date="12.01.2030",
            us_entry_date="27.02.2004",
        )
        self.assertEqual(
            get_pdf_value(fields, "document_expiration_date"),
            "01/12/2030",
        )
        self.assertEqual(get_pdf_value(fields, "us_entry_date"), "02/27/2004")


if __name__ == "__main__":
    unittest.main()
