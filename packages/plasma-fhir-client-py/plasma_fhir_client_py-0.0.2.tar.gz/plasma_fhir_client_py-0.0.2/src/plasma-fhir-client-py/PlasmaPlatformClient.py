#
# PlasmaPlatformClient
# Copyright (c) 2024 10xDevelopment LLC
#

import requests
import base64

class RESTClient:
    def __init__(self, base_url, access_token, access_token_type, default_headers = {}):
        # Remove any trailing slashes...
        base_url = base_url.rstrip('/')

        self.base_url = base_url
        self.access_token = access_token
        self.access_token_type = access_token_type
        self.default_headers = default_headers
        self.verify_ssl = False

    # Initialize the client with no auth...
    @staticmethod
    def for_no_auth(base_url):
        return RESTClient(base_url, None, None)

    # Initialize the client with a Bearer token...
    @staticmethod
    def for_bearer_token(base_url, access_token):
        return RESTClient(base_url, access_token, "Bearer")

    # Initialize the client for Basic Auth...
    @staticmethod
    def for_basic_auth(base_url, user, pwd):
        # Create the access token by combining user/pwd...
        access_token = user + ':' + pwd
        access_token = base64.b64encode(access_token.encode('utf-8')).decode('utf-8')
        return RESTClient(base_url, access_token, "Basic")

    # Get the authorization header for this instance...
    def __get_auth_header(self):
        # Check if token or type is None...
        if (not self.access_token) or (not self.access_token_type):
            return None
        return self.access_token_type + ' ' + self.access_token

    # Adds all headers, including (1) default headers, (2) auth header, (3) any additional headers...
    def __get_all_headers(self, addl_headers):
        headers = {}

        # Default headers...
        if self.default_headers:
            headers.update(self.default_headers)

        # Auth header...
        if self.access_token and self.access_token_type:
            headers['Authorization'] = self.__get_auth_header()

        # Additional headers...
        if addl_headers:
            headers.update(addl_headers)

        return headers

    # GET
    def get(self, url, params = {}, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.get(url, params, headers=headers, verify=self.verify_ssl)

    # GET, returning JSON
    def get_json(self, url, params = {}, addl_headers = {}):
        response = self.get(url, params, addl_headers)
        return response.json()

    # POST
    def post(self, url, data, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.post(url, data, headers=headers, verify=self.verify_ssl)

    # POST, returning JSON
    def post_json(self, url, data, addl_headers = {}):
        response = self.post(url, data, addl_headers)
        return response.json()

    # PUT
    def put(self, url, data, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.put(url, data, headers=headers, verify=self.verify_ssl)

    # PUT, returning JSON
    def put_json(self, url, data, addl_headers = {}):
        response = self.put(url, data, addl_headers)
        return response.json()

    # DELETE
    def delete(self, url, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.delete(url, headers=headers, verify=self.verify_ssl)

    # DELETE, returning JSON
    def delete_json(self, url, addl_headers = {}):
        response = self.delete(url, addl_headers)
        return response.json()

class FHIRClient(RESTClient):
    def __init__(self, base_url, access_token, access_token_type, default_headers = {}):
        # Initialize default headers...
        default_headers["accept"] = "application/json"
        default_headers["Content-Type"] = "application/json"

        super().__init__(base_url, access_token, access_token_type, default_headers)

    # Initialize the client with no auth...
    @staticmethod
    def for_no_auth(base_url):
        return RESTClient(base_url, None, None)

    # Initialize the client with a Bearer token...
    @staticmethod
    def for_bearer_token(base_url, access_token):
        return FHIRClient(base_url, access_token, "Bearer")

    # Initialize the client for Basic Auth...
    @staticmethod
    def for_basic_auth(base_url, user, pwd):
        # Create the access token by combining user/pwd...
        access_token = user + ':' + pwd
        access_token = base64.b64encode(access_token.encode('utf-8')).decode('utf-8')
        return FHIRClient(base_url, access_token, "Basic")

    # Read a FHIR resource...
    def readResource(self, resourceType, resourceId):
        url = self.__construct_fhir_url(resourceType, resourceId)
        return self.get_json(url)

    # Search for a FHIR resource...
    def searchResource(self, resourceType, params):
        url = self.__construct_fhir_url(resourceType)
        return self.get_json(url, params)

    # Create a FHIR resource...
    def createResource(self, resourceType, data):
        url = self.__construct_fhir_url(resourceType)
        return self.post_json(url, data)

    # Update a FHIR resource...
    def updateResource(self, resourceType, resourceId, data):
        url = self.__construct_fhir_url(resourceType, resourceId)
        return self.put_json(url, data)

    # Delete a FHIR resource...
    def deleteResource(self, resourceType, resourceId):
        url = self.__construct_fhir_url(resourceType, resourceId)
        return self.delete_json(url)

    # Construct the FHIR URL...
    def __construct_fhir_url(self, resourceType, resourceId = None, historyVersion = None):
        url = self.base_url + '/' + resourceType
        if resourceId:
            url += '/' + resourceId

        if historyVersion:
            url += '/_history/' + historyVersion

        return url

class PlasmaPlatformClient(FHIRClient):

    def __init__(self, base_url, state, code, project_id, environment_id):
        self.plasma_base_url = base_url

        default_headers = {}
        if state:
            default_headers["x-plasma-state"] = state
        if code:
            default_headers["x-plasma-code"] = code
        if project_id:
            default_headers["x-plasma-project-id"] = project_id
        if environment_id:
            default_headers["x-plasma-environment-id"] = environment_id

        fhir_base_url = base_url + '/api/plasma/fhir'
        super().__init__(fhir_base_url, None, default_headers)

    @staticmethod
    def initialize(base_url, state, code, project_id, environment_id):
        return PlasmaPlatformClient(base_url, state, code, project_id, environment_id)

    @staticmethod
    def from_state(base_url, state):
        return PlasmaPlatformClient(base_url, state, None, None, None)

    @staticmethod
    def from_code(base_url, state, code):
        return PlasmaPlatformClient(base_url, state,code, None, None)

    @staticmethod
    def for_backend(base_url, project_id, environment_id, project_secret):
        client = PlasmaPlatformClient(base_url, None, None, None, None)
        client.backend_connect(project_id, environment_id, project_secret)
        return client

    # Connect to Plasma via backend workflow...
    def backend_connect(self, project_id, environment_id, project_secret):
        # Save project/environment IDs. They will be added as headers to all requests...
        if project_id:
            self.default_headers["x-plasma-project-id"] = project_id
        if environment_id:
            self.default_headers["x-plasma-environment-id"] = environment_id

        # Send request...
        headers = { "x-plasma-project-secret": project_secret }
        url = self.plasma_base_url + '/api/plasma/sof/backend-connect'
        data = self.get_json(url, "", headers)

        # Set state and code headers...
        if data["state"]:
            self.default_headers["x-plasma-state"] = data["state"]
        if data["code"]:
            self.default_headers["x-plasma-code"] = data["code"]

        # Return result...
        return data

    # Get the current user...
    def whoami(self, read_fhir_user):
        url = self.plasma_base_url + '/api/plasma/sof/whoami'
        if read_fhir_user:
            url += '?readFhirUser=1'
        return self.get_json(url)