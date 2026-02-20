import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)

FILE_PATH = r'C:\Users\MSII\OneDrive\Desktop\error handling\reservation json.json'

htmlhandle = """
<!DOCTYPE html>
<html>
<head>
    <title>Reservation Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        h2 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 30px; background: #fff; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #007bff; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .error { color: white; background: #dc3545; padding: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    {% if error %}
        <div class="error">
            <h1>Error Handling Alert</h1>
            <p>{{ error }}</p>
        </div>
    {% else %}
        <h2>PRIMARY TABLE (RESERVATIONS)</h2>
        <table>
            <tr><th>PK_id</th><th>Status</th><th>Check-In</th><th>Check-Out</th></tr>
            <tr>
                <td>{{ res.PK_id }}</td>
                <td>{{ res.status }}</td>
                <td>{{ res.check_in }}</td>
                <td>{{ res.check_out }}</td>
            </tr>
        </table>

        <h2>JOINED TABLE (GUEST DETAILS)</h2>
        <table>
            <tr><th>FK_Reservation_id</th><th>Guest Name</th><th>Email</th></tr>
            <tr>
                <td>{{ guest.FK_reservation_id }}</td>
                <td>{{ guest.guest_name }}</td>
                <td>{{ guest.email }}</td>
            </tr>
        </table>

        <h2>JOINED TABLE (BILLING SUMMARY)</h2>
        <table>
            <tr><th>FK_Reservation_id</th><th>Type</th><th>Amount</th><th>Currency</th></tr>
            {% for item in amounts %}
            <tr>
                <td>{{ item.FK_reservation_id }}</td>
                <td>{{ item.type }}</td>
                <td>{{ item.amount }}</td>
                <td>{{ item.currency }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    try:
        if not os.path.exists(FILE_PATH):
            raise FileNotFoundError("Specified path not have file.")

        with open(FILE_PATH, 'r') as f:
            data = json.load(f)

        node = data.get("node", {})
        res_id = node.get("id")

        res_table = {
            "PK_id": res_id,
            "status": node.get("status"),
            "check_in": node.get("checkInDate"),
            "check_out": node.get("checkOutDate")
        }

        guest = node.get("primaryGuest", {})
        guest_table = {
            "FK_reservation_id": res_id,
            "guest_name": f"{guest.get('firstName', '')} {guest.get('lastName', '')}".strip(),
            "email": guest.get("emailAddress")
        }

        amounts_summary = []
        for item in node.get("amounts", {}).get("summary", []):
            amounts_summary.append({
                "FK_reservation_id": res_id,
                "type": item.get("type"),
                "amount": item.get("amount", {}).get("amount"),
                "currency": item.get("amount", {}).get("currencyCode")
            })

        return render_template_string(htmlhandle, res=res_table, guest=guest_table, amounts=amounts_summary)

    except FileNotFoundError as e:
        return render_template_string(htmlhandle, error=str(e))
    except json.JSONDecodeError:
        return render_template_string(htmlhandle, error="JSON format sahi nahi hai.")
    except Exception as e:
        return render_template_string(htmlhandle, error=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)