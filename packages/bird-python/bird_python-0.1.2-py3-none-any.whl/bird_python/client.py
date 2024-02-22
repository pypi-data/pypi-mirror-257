import json
from bird_python.error import Error
from bird_python.exceptions import ErrorException
from bird_python.http_client import HttpClient

ENDPOINT = "https://api.bird.com/"


class Client(object):
    def __init__(self, access_key, organization, workspace=None):
        self.access_key = access_key
        self.workspaces = workspace
        self.organizations = organization

    def _get_http_client(self):
        return HttpClient(ENDPOINT, self.access_key)

    def request(self, path, method="GET", params=None):
        """Builds a request, gets a response and decodes it."""
        response_text = self._get_http_client().request(path, method, params)
        if not response_text:
            return response_text

        response_json = json.loads(response_text)

        if isinstance(response_json, list):
            response_json = dict(items=response_json)

        if "errors" in response_json:
            raise (ErrorException([Error().load(e) for e in response_json["errors"]]))

        return response_json

    def contact(self, uuid):
        """Retrieve the information of a specific contact."""
        return load(self.request(f"workspaces/{self.workspaces}/contacts/" + str(uuid)))

    def contact_create(self, body=None):
        """Allows create a contact."""
        if body is None:
            body = {}
        return load(self.request(f"workspaces/{self.workspaces}/contacts", "POST", body))

    def contact_list(self):
        """Extract all contacts created in a workspace."""
        return load(self.request(f"workspaces/{self.workspaces}/contacts", "GET", None))

    def workspace_list(self):
        """Gets a list of workspaces created in an organization's account."""
        return load(self.request(f'organizations/{self.organizations}/workspaces', "GET", None))

    def workspace_list_by_id(self, uuid):
        """Gets one workspaces created in an organization's account by id."""
        return load(self.request(f'organizations/{self.organizations}/workspaces/{uuid}', "GET", None))

    def project_list(self):
        """
        Gets a list of projects created in an workspace.
        In this API you get what were previously known as templates,
        only now they can be compatible with multiple channels.
        """
        return load(self.request(f'workspaces/{self.workspaces}/projects', "GET", None))

    def project_list_by_id(self, uuid):
        """Gets one project created in an workspace by id."""
        return load(self.request(f'workspaces/{self.workspaces}/projects/{uuid}', "GET", None))

    def channel_list(self):
        """Gets a list of channels created in an workspace."""
        return load(self.request(f'workspaces/{self.workspaces}/channels', "GET", None))

    def channel_list_by_id(self, uuid):
        """Gets one channel created in an workspace by id."""
        return load(self.request(f'workspaces/{self.workspaces}/channels/{uuid}', "GET", None))

    def channel_template_list(self, project_id):
        """Gets a list of channels template created in an workspace."""
        return load(self.request(f'workspaces/{self.workspaces}/projects/{project_id}/channel-templates', "GET", None))

    def channel_template_list_by_id(self, project_id, uuid):
        """Gets one channel template created in an workspace by id."""
        return load(self.request(f'workspaces/{self.workspaces}/projects/{project_id}/channel-templates/{uuid}',
                                 "GET", None))

    def connector_list(self):
        """
        Gets a list of connectors created in an workspace.
        A connector can be Whatsapp, Messenger, SMS
        """
        return load(self.request(f'workspaces/{self.workspaces}/connectors', "GET", None))

    def connector_list_by_id(self, uuid):
        """Gets one connector created in an workspace by id."""
        return load(self.request(f'workspaces/{self.workspaces}/connectors/{uuid}', "GET", None))

    def send_message(self, channels_id: str = '', body: json = ''):
        """
        Allows you to send a message through a channel.
        :param channels_id: ID of the channel through which you want to send the message
        :param body: Body of the message in json, which contains all the information necessary to send the message
        """
        return load(self.request(f'workspaces/{self.workspaces}/channels/{channels_id}/messages', "POST", body))

    def webhook_event_list(self):
        """Gets a list of webhooks available in an workspace."""
        return load(self.request(f'workspaces/{self.workspaces}/available-webhooks', "GET", None))

    def webhook_create(self, body=None):
        """Allows create a webhook based in a event of available webhook list."""
        return load(self.request(f'organizations/{self.organizations}/workspaces/'
                                 f'{self.workspaces}/webhook-subscriptions', "POST", body))


def load(data):
    return json.loads(json.dumps(data))
