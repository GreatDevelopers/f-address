import frappe
import requests

@frappe.whitelist()
def get_address_from_coordinates(lat, lon):
    """Fetch address from OpenStreetMap using latitude & longitude"""
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"

    headers = {
        "User-Agent": "contact_address_app/1.0 (sukh.singhlotey@gmail.com)", 
        "Accept-Language": "en"  
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 403:
            frappe.throw("Error: OpenStreetMap API returned 403 Forbidden. Try using a different network or add a proper User-Agent header.")

        if response.status_code != 200:
            frappe.throw(f"Error: Received {response.status_code} from OpenStreetMap API")

        data = response.json()
        if "display_name" in data:
            return data["display_name"]
        else:
            frappe.throw("Error: Address not found in API response")

    except requests.exceptions.RequestException as e:
        frappe.throw(f"Network Error: {str(e)}")

    except requests.exceptions.JSONDecodeError:
        frappe.throw("Error: Unable to parse JSON from OpenStreetMap API")
