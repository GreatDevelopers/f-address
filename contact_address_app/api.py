import frappe
import requests

@frappe.whitelist()
def get_address_from_coordinates(lat, lon):
    """Fetch detailed address from OpenStreetMap using latitude & longitude"""
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
        if "address" in data:
            address_data = data["address"]

            return {
                "road": address_data.get("road", ""),
                "suburb": address_data.get("suburb", ""),
                "city": address_data.get("city", ""),
                "state": address_data.get("state", ""),
                "county": address_data.get("county", ""),
                "country": address_data.get("country", ""),
                "pincode": address_data.get("postcode", ""),
                "country_code": address_data.get("country_code", ""),
            }
        else:
            frappe.throw("Error: Address details not found in API response")

    except requests.exceptions.RequestException as e:
        frappe.throw(f"Network Error: {str(e)}")

    except requests.exceptions.JSONDecodeError:
        frappe.throw("Error: Unable to parse JSON from OpenStreetMap API")
