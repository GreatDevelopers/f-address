import frappe
import requests

@frappe.whitelist()
def get_address_from_coordinates(lat, lon):
    try:
        headers = {
            "User-Agent": "contact_address_app (sukh.singhlotey@gmail.com)"
        }

        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}",
            headers=headers
        )

        if response.status_code != 200:
            frappe.throw(f"Failed to fetch address. Status Code: {response.status_code}")

        data = response.json()

        if "address" not in data:
            frappe.throw("Address data not found in response.")

        address_data = data["address"]

        road = address_data.get("road", "")[:140] 
        suburb = address_data.get("suburb", "")[:140]
        city_district = address_data.get("city_district", "")[:140]
        city = address_data.get("city", "")[:140]
        state = address_data.get("state", "")[:140]
        county = address_data.get("ISO3166-2-lvl4", "")[:140]
        pincode = address_data.get("postcode", "")[:140]
        country = address_data.get("country", "")[:140]

        full_address = f"{road}, {suburb}, {city_district}, {city}, {state}, {pincode}, {country}".strip(", ")

        frappe.log_error(f"Fetched Address Data: {address_data}", "get_address_from_coordinates")
        frappe.log_error(f"Formatted Address: {full_address}", "get_address_from_coordinates")

        address_doc = frappe.get_doc({
            "doctype": "Address",
            "address_line1": full_address,  
            "address_line2": city_district,
            "city": city,
            "county": county,
            "state": state,
            "country": country,
            "pincode": pincode,
            "email_id": "sukh.singhlotey@gmail.com",
            "phone": "",
            "fax": "",
        })

        address_doc.insert(ignore_permissions=True) 

        return {"status": "success", "message": "Address saved successfully!"}

    except Exception as e:
        frappe.log_error(f"Error saving address: {str(e)}", "get_address_from_coordinates")
        return {"status": "error", "message": str(e)}
