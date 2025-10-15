import requests as r
import json

def send_message(_recipients):
	return r.post(
		"https://api.mailgun.net/v3/karddatamigration.online/messages",
		auth=("api", "b0400a5899166a36e0b87f9112b39fcc-a26b1841-a6f9d676"),
		data={"from": "Data Migration Support <postmaster@karddatamigration.online>",
			"to": "Support <postmaster@karddatamigration.online>",
			"bcc": _recipients,
			"subject": "HR Deletion Complete",
			"template": "hr deletion complete",
			"h:X-Mailgun-Variables":  json.dumps({"test": ''})})