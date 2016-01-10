import pprint

from apiclient.discovery import build

def main():
  # Build a service object for interacting with the API.
  api_root = 'http://localhost:8001/_ah/api'
  api = 'helloworld'
  version = 'v1'
  discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)

  service = build(api, version, discoveryServiceUrl=discovery_url)

  print str(service)

  # Fetch all greetings and print them out.
  response = service.greetings().listGreeting().execute()
  print str(response)
  pprint.pprint(response)

  # Fetch a single greeting and print it out.
  #response = service.greetings().get(id='9001').execute()
  #pprint.pprint(response)


if __name__ == '__main__':
  main()


'''
{
 "kind": "discovery#restDescription",
 "etag": "\"u_zXkMELIlX4ktyNbM2XKD4vK8E/dnMC5HusvhOfu8j0Nqzw1PoOVJU\"",
 "discoveryVersion": "v1",
 "id": "helloworld:v1",
 "name": "helloworld",
 "version": "v1",
 "description": "Helloworld API v1.",
 "icons": {
  "x16": "http://www.google.com/images/icons/product/search-16.gif",
  "x32": "http://www.google.com/images/icons/product/search-32.gif"
 },
 "protocol": "rest",
 "baseUrl": "http://localhost:8080/_ah/api/helloworld/v1/",
 "basePath": "/_ah/api/helloworld/v1/",
 "rootUrl": "http://localhost:8080/_ah/api/",
 "servicePath": "helloworld/v1/",
 "batchPath": "batch",
 "parameters": {
  "alt": {
   "type": "string",
   "description": "Data format for the response.",
   "default": "json",
   "enum": [
    "json"
   ],
   "enumDescriptions": [
    "Responses with Content-Type of application/json"
   ],
   "location": "query"
  },
  "fields": {
   "type": "string",
   "description": "Selector specifying which fields to include in a partial response.",
   "location": "query"
  },
  "key": {
   "type": "string",
   "description": "API key. Your API key identifies your project and provides you with API access, quota, and reports. Required unless you provide an OAuth 2.0 token.",
   "location": "query"
  },
  "oauth_token": {
   "type": "string",
   "description": "OAuth 2.0 token for the current user.",
   "location": "query"
  },
  "prettyPrint": {
   "type": "boolean",
   "description": "Returns response with indentations and line breaks.",
   "default": "true",
   "location": "query"
  },
  "quotaUser": {
   "type": "string",
   "description": "Available to use for quota purposes for server-side applications. Can be any arbitrary string assigned to a user, but should not exceed 40 characters. Overrides userIp if both are provided.",
   "location": "query"
  },
  "userIp": {
   "type": "string",
   "description": "IP address of the site where the request originates. Use this if you want to enforce per-user limits.",
   "location": "query"
  }
 },
 "auth": {
  "oauth2": {
   "scopes": {
    "https://www.googleapis.com/auth/userinfo.email": {
     "description": "View your email address"
    }
   }
  }
 },
 "schemas": {
  "HelloGreeting": {
   "id": "HelloGreeting",
   "type": "object",
   "description": "Greeting that stores a message.",
   "properties": {
    "message": {
     "type": "string"
    }
   }
  },
  "HelloGreetingCollection": {
   "id": "HelloGreetingCollection",
   "type": "object",
   "description": "Collection of Greetings.",
   "properties": {
    "items": {
     "type": "array",
     "description": "Greeting that stores a message.",
     "items": {
      "$ref": "HelloGreeting"
     }
    }
   }
  }
 },
 "resources": {
  "greetings": {
   "methods": {
    "authed": {
     "id": "helloworld.greetings.authed",
     "path": "hellogreeting/authed",
     "httpMethod": "POST",
     "response": {
      "$ref": "HelloGreeting"
     },
     "scopes": [
      "https://www.googleapis.com/auth/userinfo.email"
     ]
    },
    "getGreeting": {
     "id": "helloworld.greetings.getGreeting",
     "path": "hellogreeting/{id}",
     "httpMethod": "GET",
     "parameters": {
      "id": {
       "type": "integer",
       "required": true,
       "format": "int32",
       "location": "path"
      }
     },
     "parameterOrder": [
      "id"
     ],
     "response": {
      "$ref": "HelloGreeting"
     },
     "scopes": [
      "https://www.googleapis.com/auth/userinfo.email"
     ]
    },
    "listGreeting": {
     "id": "helloworld.greetings.listGreeting",
     "path": "hellogreeting",
     "httpMethod": "GET",
     "response": {
      "$ref": "HelloGreetingCollection"
     },
     "scopes": [
      "https://www.googleapis.com/auth/userinfo.email"
     ]
    },
    "multiply": {
     "id": "helloworld.greetings.multiply",
     "path": "hellogreeting/{times}",
     "httpMethod": "POST",
     "parameters": {
      "times": {
       "type": "integer",
       "required": true,
       "format": "int32",
       "location": "path"
      }
     },
     "parameterOrder": [
      "times"
     ],
     "request": {
      "$ref": "HelloGreeting",
      "parameterName": "resource"
     },
     "response": {
      "$ref": "HelloGreeting"
     },
     "scopes": [
      "https://www.googleapis.com/auth/userinfo.email"
     ]
    }
   }
  }
 }
}
'''
