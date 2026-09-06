W7_FIELDS = {
    # Application
    "apply_new_itin": "c1_1[0]",
    "renew_itin": "c1_1[1]",

    # Reasons
    "reason_a": "c1_2[0]",
    "reason_b": "c1_3[0]",
    "reason_c": "c1_4[0]",
    "reason_d": "c1_5[0]",
    "reason_d_relationship": "f1_01[0]",

    "reason_e": "c1_6[0]",
    "reason_e_name": "f1_02[0]",
    "reason_e_ssn_itin": "f1_03[0]",

    "reason_f": "c1_7[0]",
    "reason_g": "c1_8[0]",
    "reason_h": "c1_9[0]",

    "reason_h_details": "f1_04[0]",
    "treaty_country": "f1_05[0]",
    "treaty_article": "f1_06[0]",

    # Name
    "first_name": "f1_07[0]",
    "middle_name": "f1_08[0]",
    "last_name": "f1_09[0]",

    "birth_first_name": "f1_10[0]",
    "birth_middle_name": "f1_11[0]",
    "birth_last_name": "f1_12[0]",

    # Mailing address
    "mailing_street": "f1_13[0]",
    "mailing_city_country_postal": "f1_14[0]",

    # Foreign address
    "foreign_street": "f1_15[0]",
    "foreign_city_country_postal": "f1_16[0]",

    # Birth
    "date_of_birth": "f1_17[0]",
    "country_of_birth": "f1_18[0]",
    "birth_city_state": "f1_19[0]",

    "gender_male": "c1_10[0]",
    "gender_female": "c1_10[1]",

    # Other information
    "citizenship": "f1_20[0]",
    "foreign_tax_id": "f1_21[0]",
    "us_visa": "f1_22[0]",

    # Identification
    "document_passport": "c1_11[0]",
    "document_driver_license": "c1_11[1]",
    "document_uscis": "c1_11[2]",
    "document_other": "c1_11[3]",

    "document_other_description": "f1_23[0]",
    "document_issued_by": "f1_24[0]",
    "document_number": "f1_25[0]",
    "document_expiration_date": "f1_26[0]",
    "us_entry_date": "f1_27[0]",

    # Previous ITIN / IRSN
    "previous_itin_no": "c1_12[0]",
    "previous_itin_yes": "c1_12[1]",

    "itin_part_1": "f1_28[0]",
    "itin_part_2": "f1_29[0]",
    "itin_part_3": "f1_30[0]",

    "irsn_part_1": "f1_31[0]",
    "irsn_part_2": "f1_32[0]",
    "irsn_part_3": "f1_33[0]",

    "previous_first_name": "f1_34[0]",
    "previous_middle_name": "f1_35[0]",
    "previous_last_name": "f1_36[0]",

    # Institution
    "institution_name": "f1_37[0]",
    "institution_city_state": "f1_38[0]",
    "length_of_stay": "f1_39[0]",

    # Sign / delegate
    "phone_number": "f1_40[0]",
    "delegate_name": "f1_41[0]",

    "delegate_parent": "c1_13[0]",
    "delegate_power_of_attorney": "c1_13[1]",
    "delegate_court_guardian": "c1_13[2]",

    # Acceptance Agent
    "agent_phone": "f1_42[0]",
    "agent_fax": "f1_43[0]",
    "agent_name_title": "f1_44[0]",
    "agent_company": "f1_45[0]",
    "agent_ein": "f1_46[0]",
    "agent_ptin": "f1_47[0]",
    "agent_office_code": "f1_48[0]",
}


W7_CHECKBOX_VALUES = {
    "apply_new_itin": "/2",
    "renew_itin": "/1",

    "reason_a": "/1",
    "reason_b": "/1",
    "reason_c": "/1",
    "reason_d": "/1",
    "reason_e": "/1",
    "reason_f": "/1",
    "reason_g": "/1",
    "reason_h": "/1",

    "gender_male": "/1",
    "gender_female": "/2",

    "document_passport": "/1",
    "document_driver_license": "/2",
    "document_uscis": "/3",
    "document_other": "/4",

    "previous_itin_no": "/1",
    "previous_itin_yes": "/2",

    "delegate_parent": "/1",
    "delegate_power_of_attorney": "/2",
    "delegate_court_guardian": "/3",
}
