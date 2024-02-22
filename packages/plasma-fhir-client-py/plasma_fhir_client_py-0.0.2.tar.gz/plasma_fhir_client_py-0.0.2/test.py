from PlasmaPlatformClient import PlasmaPlatformClient
import json

print("Start")

# CigStopper...

#baseUrl = "https://plasma.smart-on-fhir.com"
baseUrl = "https://localhost:3000"
projectId = "167"
projectSecret = "clstfqhig0001jj08zy641kk4"
envEpicId = "286"
client = PlasmaPlatformClient.for_backend(baseUrl, projectId, envEpicId, projectSecret)

# Print a JSON version of client...
print(json.dumps(client, default=lambda o: o.__dict__, sort_keys=True, indent=4))


# Try to read patient...
patientId = "eD.LxhDyX35TntF77l7etUA3"
patientRead = client.readResource("Patient", patientId)
#print(json.dumps(patientRead, default=lambda o: o.__dict__, sort_keys=True, indent=4))

# Try to search for a patient...
patientSearch = client.searchResource("Patient", { "given": "Jason", "family": "Argonaut", "birthdate": "1985-08-01" })
print(json.dumps(patientSearch, default=lambda o: o.__dict__, sort_keys=True, indent=4))




print("End")