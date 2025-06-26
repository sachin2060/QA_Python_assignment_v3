import csv
import os

# Initialize list to store assets (max 10 records)
assets = []

# Valid options for asset_type and asset_status
VALID_TYPES = ["laptop", "desktop", "printer", "software"]
VALID_STATUSES = ["active", "inactive", "repair"]


# Function to validate asset inputs
def validate_asset(asset_id, asset_type, asset_brand, asset_model, asset_status, asset_location, is_new=True):
    errors = []

    # Validate asset_id
    try:
        asset_id = int(asset_id)
        if asset_id <= 0:
            errors.append("Asset ID must be a positive integer.")
        if is_new and any(asset['asset_id'] == asset_id for asset in assets):
            errors.append("Asset ID must be unique.")
    except ValueError:
        errors.append("Asset ID must be an integer.")

    # Validate asset_type
    if asset_type.lower() not in VALID_TYPES:
        errors.append(f"Asset Type must be one of: {', '.join(VALID_TYPES)}")

    # Validate asset_brand and asset_model
    if not (asset_brand and len(asset_brand.strip()) <= 50):
        errors.append("Brand must be a non-empty string, max 50 characters.")
    if not (asset_model and len(asset_model.strip()) <= 50):
        errors.append("Model must be a non-empty string, max 50 characters.")

    # Validate asset_status
    if asset_status.lower() not in VALID_STATUSES:
        errors.append(f"Status must be one of: {', '.join(VALID_STATUSES)}")

    # Validate asset_location
    if not (asset_location and len(asset_location.strip()) <= 50):
        errors.append("Location must be a non-empty string, max 50 characters.")

    return errors


# Function to add a new asset
def add_asset():
    if len(assets) >= 10:
        print("Maximum capacity of 10 assets reached!")
        return

    asset_id = input("Enter Asset ID: ")
    asset_type = input(f"Enter Asset Type ({', '.join(VALID_TYPES)}): ")
    asset_brand = input("Enter Brand: ")
    asset_model = input("Enter Model: ")
    asset_status = input(f"Enter Status ({', '.join(VALID_STATUSES)}): ")
    asset_location = input("Enter Location: ")

    errors = validate_asset(asset_id, asset_type, asset_brand, asset_model, asset_status, asset_location)
    if errors:
        print("Validation Errors:")
        for error in errors:
            print(f"- {error}")
        return

    asset = {
        'asset_id': int(asset_id),
        'asset_type': asset_type.lower(),
        'asset_brand': asset_brand.strip(),
        'asset_model': asset_model.strip(),
        'asset_status': asset_status.lower(),
        'asset_location': asset_location.strip()
    }
    assets.append(asset)
    print("Asset added successfully!")


# Function to edit an existing asset
def edit_asset():
    if not assets:
        print("No assets to edit!")
        return

    asset_id = input("Enter Asset ID to edit: ")
    try:
        asset_id = int(asset_id)
    except ValueError:
        print("Validation Error: Asset ID must be an integer.")
        return

    # Find asset by ID
    for asset in assets:
        if asset['asset_id'] == asset_id:
            print("\nCurrent Asset Details:")
            print(f"ID: {asset['asset_id']}, Type: {asset['asset_type']}, Brand: {asset['asset_brand']}, "
                  f"Model: {asset['asset_model']}, Status: {asset['asset_status']}, Location: {asset['asset_location']}")

            # Prompt for new values (press Enter to keep current value)
            new_type = input(f"Enter new Type ({', '.join(VALID_TYPES)}) [Enter to keep '{asset['asset_type']}']: ") or \
                       asset['asset_type']
            new_brand = input(f"Enter new Brand [Enter to keep '{asset['asset_brand']}']: ") or asset['asset_brand']
            new_model = input(f"Enter new Model [Enter to keep '{asset['asset_model']}']: ") or asset['asset_model']
            new_status = input(
                f"Enter new Status ({', '.join(VALID_STATUSES)}) [Enter to keep '{asset['asset_status']}']: ") or asset[
                             'asset_status']
            new_location = input(f"Enter new Location [Enter to keep '{asset['asset_location']}']: ") or asset[
                'asset_location']

            # Validate new values (ID remains unchanged)
            errors = validate_asset(asset_id, new_type, new_brand, new_model, new_status, new_location, is_new=False)
            if errors:
                print("Validation Errors:")
                for error in errors:
                    print(f"- {error}")
                return

            # Update asset
            asset['asset_type'] = new_type.lower()
            asset['asset_brand'] = new_brand.strip()
            asset['asset_model'] = new_model.strip()
            asset['asset_status'] = new_status.lower()
            asset['asset_location'] = new_location.strip()
            print("Asset updated successfully!")
            return

    print(f"No asset found with ID {asset_id}")


# Function to display all assets
def display_assets():
    if not assets:
        print("No assets to display!")
        return

    print("\nIT Asset Inventory:")
    print("-" * 80)
    print(f"{'ID':<8} {'Type':<12} {'Brand':<15} {'Model':<15} {'Status':<12} {'Location':<15}")
    print("-" * 80)

    for asset in assets:
        print(f"{asset['asset_id']:<8} {asset['asset_type']:<12} {asset['asset_brand']:<15} "
              f"{asset['asset_model']:<15} {asset['asset_status']:<12} {asset['asset_location']:<15}")
    print()


# Function to save assets to CSV
def save_to_csv():
    filename = 'it_assets.csv'
    fieldnames = ['asset_id', 'asset_type', 'asset_brand', 'asset_model', 'asset_status', 'asset_location']

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for asset in assets:
                writer.writerow(asset)
        print(f"Assets saved to {filename}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")


# Function to load assets from CSV
def load_from_csv():
    filename = 'it_assets.csv'
    assets.clear()

    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if len(assets) < 10:  # Limit to 10 assets
                        errors = validate_asset(row['asset_id'], row['asset_type'], row['asset_brand'],
                                                row['asset_model'], row['asset_status'], row['asset_location'],
                                                is_new=True)
                        if not errors:
                            row['asset_id'] = int(row['asset_id'])
                            assets.append(row)
                        else:
                            print(f"Skipping invalid asset (ID {row['asset_id']}): {', '.join(errors)}")
            print(f"Assets loaded from {filename}")
        except IOError as e:
            print(f"Error loading CSV: {e}")
    else:
        print("No existing CSV file found.")


# Main menu
def main():
    load_from_csv()  # Load existing assets at start

    while True:
        print("\nIT Asset Management System")
        print("1. Add New Asset")
        print("2. Edit Asset")
        print("3. Display All Assets")
        print("4. Save to CSV")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_asset()
        elif choice == '2':
            edit_asset()
        elif choice == '3':
            display_assets()
        elif choice == '4':
            save_to_csv()
        elif choice == '5':
            save_to_csv()
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please try again.")


# Run the program
if __name__ == "__main__":
    main()