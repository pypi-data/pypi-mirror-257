def check_duplicates(df):
    duplicate_ids = df[df.duplicated(subset="transaction_id", keep=False)]
    print("Going into the check_duplicates function")
    if not duplicate_ids.empty:
        print(
            "⚠️ Hold on! Duplicate transaction IDs found. Checking for floor_number conflicts. 🕵️‍♂️"
        )

        # Check for conflicts in floor_number
        conflicting_floor = duplicate_ids[
            duplicate_ids.duplicated(subset=["transaction_id", "floor_no"], keep=False)
        ]

        if not conflicting_floor.empty:
            print("⚠️ Conflicting floor numbers for the same transaction ID:")
            for _, row in conflicting_floor.iterrows():
                print(
                    f"   Transaction ID: {row['transaction_id']}, Floor Number: {row['floor_no']}"
                )
        else:
            print(
                "✅ No conflicts in floor numbers. Duplicate transaction IDs have different floor numbers. 🚀"
            )
    else:
        print(
            "✅ No duplicate transaction IDs found. Proceeding without checking conflicts."
        )
