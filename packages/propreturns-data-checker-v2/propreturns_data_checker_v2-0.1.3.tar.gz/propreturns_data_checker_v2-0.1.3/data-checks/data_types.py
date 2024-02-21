def check_data_types(df, data_type):
    """
    Check data types of columns in a DataFrame against expected data types.

    Parameters:
    - df: pandas DataFrame
    - data_type: string specifying the type of data ('sale' or 'lease')

    Returns:
    - List of columns with data type mismatches
    """

    sale_data_types = {
        "village_name": "object",
        "document_name": "object",
        "transaction_price": "float64",
        "market_price": "float64",
        "other_information": "object",
        "area_in_sq_ft": "float64",
        "seller_name_and_address": "object",
        "buyer_name_and_address": "object",
        "submission_date": "datetime64[ns]",
        "transaction_date": "datetime64[ns]",
        "document_number": "object",
        "stamp_duty": "float64",
        "registration_fee": "float64",
        "price_per_sq_ft_acc_to_transaction_price": "float64",
        "price_per_sq_ft_acc_to_market_price": "float64",
        "asset_type": "object",
        "parent_building_name": "object",
        "seller_name": "object",
        "buyer_name": "object",
        "unit_no": "object",
        "floor_no": "object",
        "buyer_company_name": "object",
        "seller_company_name": "object",
        "transaction_id": "object",
        "price_per_sq_ft_acc_to_actual_price": "float64",
        "actual_transaction_price": "float64",
        "building_id": "float64",
        "wing": "object",
        "building_no": "object",
        "transaction_source": "object",
        "micromarket": "object",
        "chargeable_area": "float64",
        "developer_name": "object",
        "lease_start_date": "datetime64[ns]",
        "expiry_date": "datetime64[ns]",
        "tenant_industry_type": "object",
        "carpet_area": "object",
        "landlord/_licensors'_lock-in_period": "object",
        "tenant/_licensee's_lock-_in_period": "object",
        "deposit": "object",
        "rent_free_period": "object",
        "condition_of_space": "object",
        "furnished_rate": "float64",
        "cam_charge": "float64",
        "cam_paid_by": "object",
        "property_tax": "float64",
        "property_tax_paid_by": "object",
        "current_rent_per_sq_ft": "object",
        "registration_amount": "float64",
        "car_parking_slots": "object",
        "car_parking_charges": "float64",
        "next_escalation_date": "object",
        "next_escalation_rate": "object",
        "building_name": "object",
        "wing_id": "int64",
        "builtup_area": "float64",
        "carpet_area_source": "object",
        "builtup_area_source": "object",
    }
    # Example data types for lease data
    lease_data_types = {
        "village_name": "object",
        "document_name": "object",
        "rent_per_month": "float64",
        "deposit": "object",
        "other_information": "object",
        "area_in_sq_ft": "float64",
        "seller_name_and_address": "object",
        "buyer_name_and_address": "object",
        "submission_date": "datetime64[ns]",
        "transaction_date": "datetime64[ns]",
        "document_number": "object",
        "stamp_duty": "float64",
        "registration_fee": "float64",
        "asset_type": "object",
        "parent_building_name": "object",
        "buyer_name": "object",
        "seller_name": "object",
        "extracted_tenure": "float64",
        "expiry_date": "object",
        "assumed_months_for_expiry_date": "object",
        "rental_terms_extracted": "object",
        "unit_no": "object",
        "floor_no": "object",
        "has_extra_area_info": "object",
        "transaction_id": "object",
        "building_id": "float64",
        "buyer_company_name": "object",
        "seller_company_name": "object",
        "registration_fees": "float64",
        "wing": "object",
        "building_no": "object",
        "transaction_source": "object",
        "micromarket": "object",
        "chargeable_area": "float64",
        "rent_per_sq_ft": "float64",
        "developer_name": "object",
        "tenant_industry_type": "object",
        "carpet_area": "object",
        "landlord/_licensors'_lock-in_period": "object",
        "tenant/_licensee's_lock-_in_period": "object",
        "rent_free_period": "object",
        "condition_of_space": "object",
        "furnished_rate": "float64",
        "cam_charge": "float64",
        "cam_paid_by": "object",
        "property_tax": "float64",
        "property_tax_paid_by": "object",
        "current_rent_per_sq_ft": "float64",
        "registration_amount": "float64",
        "car_parking_slots": "object",
        "car_parking_charges": "float64",
        "next_escalation_date": "datetime64[ns]",
        "next_escalation_rate": "float64",
        "building_name": "object",
        "wing_id": "int64",
        "builtup_area": "float64",
        "carpet_area_source": "object",
        "builtup_area_source": "object",
    }

    expected_data_types = (
        sale_data_types if data_type.lower() == "sale" else lease_data_types
    )

    mismatched_columns = [
        (col, expected_data_types[col])
        for col in df.columns
        if col in expected_data_types and str(df[col].dtype) != expected_data_types[col]
    ]

    return mismatched_columns if mismatched_columns else []
