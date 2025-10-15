import requests as r
import json

def send_message(_recipients):
	return r.post(
		"Redacted" ##Removed as its the URL of Mail Gun,
		auth=("api", "Redacted" ## Remove as this is the API Key),
		data={"from": "Data Migration Support <postmaster@karddatamigration.online>",
			"to": "Support <postmaster@karddatamigration.online>",
			"bcc": _recipients,
			"subject": "HR Deletion Complete",
			"template": "hr deletion complete",

			"h:X-Mailgun-Variables":  json.dumps({"test": ''})})
