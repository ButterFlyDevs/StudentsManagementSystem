import pprint

from apiclient.discovery import build

def main():
  # Build a service object for interacting with the API.
  api_root = 'localhost/_ah/helloworld'
  api = 'guestbook'
  version = 'v0.2'
  discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
  service = build(api, version, discoveryServiceUrl=discovery_url)

  # Fetch all greetings and print them out.
  response = service.greetings().list().execute()
  pprint.pprint(response)

  # Fetch a single greeting and print it out.
  response = service.greetings().get(id='9001').execute()
  pprint.pprint(response)

if __name__ == '__main__':
  main()
