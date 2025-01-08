import requests
import json

API_BASE_URL = "http://127.0.0.1:5000"  # Port disesuaikan dengan Flask

def print_response(response):
    """Print response data in a formatted way."""
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

# Laptop related functions
def create_laptop():
    """Send POST request to create a new laptop."""
    print("Enter laptop details:")
    brand = input("Brand: ")
    model = input("Model: ")
    price = float(input("Price: "))
    specs = input("Specs: ")
    payload = {
        "brand": brand,
        "model": model,
        "price": price,
        "specs": specs
    }
    response = requests.post(f"{API_BASE_URL}/laptops", json=payload)
    print_response(response)

def read_all_laptops():
    """Send GET request to fetch all laptops."""
    response = requests.get(f"{API_BASE_URL}/laptops")
    print_response(response)

def read_laptop_by_id():
    """Send GET request to fetch a laptop by ID."""
    laptop_id = input("Enter laptop ID: ")
    response = requests.get(f"{API_BASE_URL}/laptops/{laptop_id}")
    print_response(response)

def update_laptop():
    """Send PUT request to update an existing laptop."""
    laptop_id = input("Enter laptop ID to update: ")
    print("Enter new details:")
    brand = input("Brand: ")
    model = input("Model: ")
    price = float(input("Price: "))
    specs = input("Specs: ")
    payload = {
        "brand": brand,
        "model": model,
        "price": price,
        "specs": specs
    }
    response = requests.put(f"{API_BASE_URL}/laptops/{laptop_id}", json=payload)
    print_response(response)

def delete_laptop():
    """Send DELETE request to delete a laptop."""
    laptop_id = input("Enter laptop ID to delete: ")
    response = requests.delete(f"{API_BASE_URL}/laptops/{laptop_id}")
    print_response(response)

def main():
    """Main menu for CRUD operations."""
    while True:
        print("\nMenu:")
        print("1. Tambah Laptop")
        print("2. Lihat Laptop")
        print("3. Lihat Laptop Berdasarkan ID")
        print("4. Update Laptop")
        print("5. Hapus Laptop")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_laptop()
        elif choice == "2":
            read_all_laptops()
        elif choice == "3":
            read_laptop_by_id()
        elif choice == "4":
            update_laptop()
        elif choice == "5":
            delete_laptop()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
