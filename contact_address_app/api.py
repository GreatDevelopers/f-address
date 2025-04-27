import frappe
import requests
from openlocationcode import openlocationcode as olc  # Import the library

@frappe.whitelist()
def get_address_from_coordinates(lat, lon):
    """Fetch detailed address from OpenStreetMap and generate Google Plus Code using latitude & longitude"""
    # Existing OpenStreetMap API call
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"

    headers = {
        "User-Agent": "contact_address_app/1.0 (sukh.singhlotey@gmail.com)",
        "Accept-Language": "en"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 403:
            frappe.throw("Error: OpenStreetMap API returned 403 Forbidden. Check your network or User-Agent header.")

        if response.status_code != 200:
            frappe.throw(f"Error: Received {response.status_code} from OpenStreetMap API")

        data = response.json()
        address_data = data.get("address", {})

        # Generate Google Plus Code from coordinates
        plus_code = olc.encode(float(lat), float(lon))  # Convert lat/lon to float and generate Plus Code

        # Return address data plus the new Plus Code
        return {
            "road": address_data.get("road", ""),
            "suburb": address_data.get("suburb", ""),
            "city": address_data.get("city", ""),
            "state": address_data.get("state", ""),
            "county": address_data.get("county", ""),
            "country": address_data.get("country", ""),
            "pincode": address_data.get("postcode", ""),
            "country_code": address_data.get("country_code", ""),
            "plus_code": plus_code  # Add the Plus Code to the response
        }

    except requests.exceptions.RequestException as e:
        frappe.throw(f"Network Error: {str(e)}")

    except requests.exceptions.JSONDecodeError:
        frappe.throw("Error: Unable to parse JSON from OpenStreetMap API")
