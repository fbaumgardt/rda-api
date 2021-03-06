class swagger:

    @classmethod
    def index(cls, url):
        return """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="x-ua-compatible" content="IE=edge">
        <title>Swagger UI</title>
    </head>

    <body>
        <iframe  style="position:fixed; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" src="http://rdacollectionswg.github.io/apidocs/index.html?url={}"></iframe>
    </body>
</html>""".format(url.replace("/","%2F")).encode()

    @classmethod
    def json(cls, schemes, host, port, base_path):
        return """{{
    "swagger": "2.0",
    "info": {{
        "title": "RDA Collections API",
        "description": "API Strawman for RDA Research Data Collections WG",
        "version": "1.0.0"
    }},
    "schemes": [
        {}
    ],
    "host": "{}",
    "port": "{}",
    "basePath": "{}",
  "produces": [
    "application/json"
  ],
  "securityDefinitions": {{
    "oauth": {{
      "type": "oauth2",
      "authorizationUrl": "http://example.org/oauth/authorize",
      "flow": "accessCode",
      "tokenUrl": "http://example.org/oauth/token",
      "scopes": {{
        "write": "Can write collections",
        "read": "Can read collections",
        "modify": "Can modify collections"
      }}
    }}
  }},
  "paths": {{
    "/features": {{
      "get": {{
        "summary": "Gets the service-level features.",
        "description": "This request returns the service-level features. Examples of service-level features might include whether or not the service supports assignment of PIDs for collection members, whether it supports pagination and cursors, whether it enforces  access controls, etc.",
        "tags": [
          "Service"
        ],
        "responses": {{
          "200": {{
            "description": "Service Level Features",
            "schema": {{
              "$ref": "#/definitions/ServiceFeatures"
            }}
          }}
        }}
      }}
    }},
    "/collections": {{
      "get": {{
        "summary": "Get a list of all collections",
        "description": "This request returns a list of the collections provided by this service.  This may be a complete list, or if the service features include support for pagination, the cursors in the response may be used to iterate backwards and forwards through pages of partial results. Query parameters may be used to supply filtering criteria for the response. When combining filters of different types, the boolean AND will be used. When combining multiple instances of filters of the same type, the boolean OR will be used.",
        "parameters": [
          {{
            "name": "f_modelType",
            "in": "query",
            "description": "Filter response by the modelType property of the collection.",
            "required": false,
            "type": "string",
            "collectionFormat": "multi"
          }},
          {{
            "name": "f_memberType",
            "in": "query",
            "description": "Filter response by the data type of contained collection member. A collection will meet this requirement if any of its members are of the requested type.",
            "required": false,
            "type": "string",
            "collectionFormat": "multi"
          }},
          {{
            "name": "f_ownership",
            "in": "query",
            "description": "Filter response by the ownership property of the collection",
            "type": "string",
            "collectionFormat": "multi"
          }},
          {{
            "name": "cursor",
            "in": "query",
            "description": "cursor for iterating a prior response to this query",
            "type": "string"
          }}
        ],
        "tags": [
          "Collections"
        ],
        "responses": {{
          "200": {{
            "description": "A resultset containing a list of collection objects.",
            "schema": {{
              "$ref": "#/definitions/CollectionResultSet"
            }}
          }},
          "400": {{
            "description": "Invalid Input. The query was malformed.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "post": {{
        "summary": "Create a new collection.",
        "description": "This request adds a new collection to the collection store. The Collection Object properties must be supplied in the  body of the request. ",
        "parameters": [
          {{
            "name": "content",
            "in": "body",
            "description": "The properties of the collection.",
            "required": true,
            "schema": {{
              "type": "array",
              "items": {{
                "$ref": "#/definitions/CollectionObject"
              }}
            }}
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "write"
            ]
          }}
        ],
        "responses": {{
          "201": {{
            "description": "Successful creation",
            "schema": {{
              "type": "array",
              "items": {{
                "$ref": "#/definitions/CollectionObject"
              }}
            }}
          }},
          "202": {{
            "description": "Accepted create request. Empty response body. (For asyncrhonous requests,  if supported by the service features)."
          }},
          "400": {{
            "description": "Invalid Input. The collection properties were malformed or invalid.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "409": {{
            "description": "Conflict. A collection with the same ID as the one posted already exists.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}": {{
      "get": {{
        "summary": "Get the properties of a specific collection.",
        "description": "This request returns the Collection Object Properties for the collection identified by the provided id.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }}
        ],
        "tags": [
          "Collections"
        ],
        "responses": {{
          "200": {{
            "description": "The requested collection",
            "schema": {{
              "$ref": "#/definitions/CollectionObject"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The requested collection was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "put": {{
        "summary": "Update the properties of a Collection Object",
        "description": "This request updates the properties of the collection identified by the provided id. The updated collection properties must be supplied in the body of the request. The response may differ depending upon whether or not the  service features include support for syncrhonous actions.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Persistent identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "content",
            "in": "body",
            "description": "The properties of the collection to be updated.",
            "required": true,
            "schema": {{
              "$ref": "#/definitions/CollectionObject"
            }}
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "modify"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "Successful update, returns the updated collection.",
            "schema": {{
              "$ref": "#/definitions/CollectionObject"
            }}
          }},
          "202": {{
            "description": "Accepted update request. Empty response body. (For asynchronous requests if supported by service features.)"
          }},
          "400": {{
            "description": "Invalid Input. The collection properties were malformed or invalid.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to update a collection whose metadata is not mutable.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The collection identified for update was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "delete": {{
        "summary": "Delete a collection",
        "description": "This request deletes the collection idenified by the provided id from the collection store. The response may differ depending upon whether or not the service features include support for synchronous actions.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "identifier for the collection",
            "required": true,
            "type": "string"
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "write"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "Successful deletion. Empty response body."
          }},
          "202": {{
            "description": "Accepted deletion request. Empty response body. (For asynchronous requests if supported by service features.)"
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The collection identified for deletion was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/capabilities": {{
      "get": {{
        "summary": "Get the capabilities of this collection",
        "description": "This request returns the capabilities metadata for the collection identified by the supplied id. The collection capabilities describe the actions and operations that are available for this collection.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }}
        ],
        "tags": [
          "Collections"
        ],
        "responses": {{
          "200": {{
            "description": "The collection capabilities metadata.",
            "schema": {{
              "$ref": "#/definitions/CollectionCapabilities"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The collection identified was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/ops/findMatch": {{
      "post": {{
        "summary": "Find member objects in a collection which match the supplied member object",
        "description": "This request accepts as input the complete or partial properties of a member object and returns a ResultSet containing any objects which were deemed to 'match' the supplied properties among the members of the identified collection. If the service features include support for pagination, a cursor may be supplied to iterate backwards and forwards through paged results from prior executions of this query.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "memberProperties",
            "in": "body",
            "description": "the member item properties to use when matching",
            "required": true,
            "schema": {{
              "$ref": "#/definitions/MemberItem"
            }}
          }},
          {{
            "name": "cursor",
            "in": "query",
            "type": "string",
            "description": "If the service supports pagination and a cursor was returned in a prior  response to this query, this can be used to requeste a particular page of the  results."
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "read"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "A resulset containing the matching member items from the two collections.",
            "schema": {{
              "$ref": "#/definitions/MemberResultSet"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The collection identified was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/ops/intersection/{{otherId}}": {{
      "get": {{
        "summary": "Retrieve the members at the intersection of two collections",
        "description": "This request returns a resultset containing the members at the intersection of two collections. If the service features include support for pagination, a cursor may be supplied to iterate backwards and forwards through paged results from prior executions of this query. The response may be an empty set.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the first collection in the operation",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "otherId",
            "in": "path",
            "description": "Identifier for the second collection in the operation",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "cursor",
            "in": "query",
            "type": "string",
            "description": "If the service supports pagination and a cursor was returned in a prior response to this query, this can be used to requeste a particular page of the results."
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "read"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "A resultset containing the intersection of member items from the two collections.",
            "schema": {{
              "$ref": "#/definitions/MemberResultSet"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "One or both of the requested collections was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/ops/union/{{otherId}}": {{
      "get": {{
        "summary": "Retrieve the union of two collections",
        "description": "This request returns a resultset containing the members at the union of two collections. If the service features include support for pagination, a cursor may be supplied to iterate backwards and forwards through paged results from prior executions of this query. The response may be an empty set.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the first collection in the operation",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "otherId",
            "in": "path",
            "description": "Identifier for the second collection in the operation",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "cursor",
            "in": "query",
            "type": "string",
            "description": "If the service supports pagination and a cursor was returned in a prior response to this query, this can be used to requeste a particular page of the results."
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "read"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "A resultset containing the union of member items from the two collections",
            "schema": {{
              "$ref": "#/definitions/MemberResultSet"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "One or both of the requested collections was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/ops/flatten": {{
      "get": {{
        "summary": "Flattens the collection",
        "description": "This request returns a resultset which is a flattened representation of a collection of collections into a single collection.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection to be flattened",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "cursor",
            "in": "query",
            "type": "string",
            "description": "If the service supports pagination and a cursor was returned in a prior response to this query, this can be used to requeste a particular page of the results."
          }}
        ],
        "tags": [
          "Collections"
        ],
        "security": [
          {{
            "oauth": [
              "read"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "A resultset containing the union of member items from the two collections",
            "schema": {{
              "$ref": "#/definitions/MemberResultSet"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "One or both of the requested collections was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/members": {{
      "get": {{
        "summary": "Get the members in a collection",
        "description": "This request returns the list of members contained in a collection.  This may be a complete list, or if the service features include support for pagination, the cursors in the response may be used to iterate backwards and forwards through pages of partial results. Query parameters may be used to supply filtering criteria for the response. When combining filters of different types, the boolean AND will be used. When combining multiple instances of filters of the same type, the boolean OR will be used.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "f_datatype",
            "in": "query",
            "description": "Filter response to members matching the requested datatype.",
            "required": false,
            "type": "string",
            "collectionFormat": "multi"
          }},
          {{
            "name": "f_role",
            "in": "query",
            "description": "Filter response to members who are assigned the requested role. (Only if the collection capability supportsRoles is true).",
            "required": false,
            "type": "string",
            "collectionFormat": "multi"
          }},
          {{
            "name": "f_index",
            "in": "query",
            "description": "Filter response to the members assigned the requested index. (Only if the collection capability isOrdered is true).",
            "type": "integer",
            "collectionFormat": "multi",
            "required": false
          }},
          {{
            "name": "f_dateAdded",
            "in": "query",
            "description": "Filter response to the membered added on the requestd datetime.",
            "type": "string",
            "format": "date-time",
            "required": false
          }},
          {{
            "name": "cursor",
            "in": "query",
            "description": "cursor for iterating a prior response to this query",
            "type": "string"
          }},
          {{
            "name": "expandDepth",
            "in": "query",
            "description": "expand members which are collections to this depth. may not exceed maxExpansionDepth feature setting for the service.",
            "type": "integer",
            "required": false
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "200": {{
            "description": "A resultset containing the list of member items in the identified collection.",
            "schema": {{
              "$ref": "#/definitions/MemberResultSet"
            }}
          }},
          "400": {{
            "description": "Invalid input. The filter query was malformed.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "The collection identified was not found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "post": {{
        "summary": "Add a new member item to this collection",
        "description": "This request adds a new member item to a collection. If the service features include support for PID assignment to member items, then if no id is supplied for the item it  will be assigned automatically.  ",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "content",
            "in": "body",
            "description": "The properties of the member item to add to the collection. Id may be required.",
            "required": true,
            "schema": {{
              "type": "array",
              "items": {{
                "$ref": "#/definitions/MemberItem"
              }}
            }}
          }}
        ],
        "security": [
          {{
            "oauth": [
              "write"
            ]
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "201": {{
            "description": "Successful creation",
            "schema": {{
              "type": "array",
              "items": {{
                "$ref": "#/definitions/MemberItem"
              }}
            }}
          }},
          "202": {{
            "description": "Accepted add request. Empty response body. (For asyncrhonous requests,  if supported by the service features)."
          }},
          "400": {{
            "description": "Invalid Request. Indicates that member properties were incorrect or invalid in  some way."
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to add  an item to a static collection."
          }},
          "404": {{
            "description": "Not found. The collection was not found for adding items.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "409": {{
            "description": "Conflict. A member item with the same ID as the one posted already exists.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/members/{{mid}}": {{
      "get": {{
        "summary": "Get the properties of a member item in a collection",
        "description": "This request retrieves the properties of a specific member item from a collection",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member item.",
            "required": true
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "200": {{
            "description": "The requested member",
            "schema": {{
              "$ref": "#/definitions/MemberItem"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "Not found. The requested collection or member item was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "put": {{
        "summary": "Update the properties of a collection member item.",
        "description": "This request updates the properties of a collection member item.  The updated member  properties must be supplied in the body of the request. The response may differ  depending upon whether or not the  service features include support  for asynchronous actions.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member",
            "required": true
          }},
          {{
            "name": "content",
            "in": "body",
            "description": "collection metadata",
            "required": true,
            "schema": {{
              "$ref": "#/definitions/CollectionObject"
            }}
          }}
        ],
        "tags": [
          "Members"
        ],
        "security": [
          {{
            "oauth": [
              "modify"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "Successful update. The updated member item is returned in the response.",
            "schema": {{
              "$ref": "#/definitions/MemberItem"
            }}
          }},
          "202": {{
            "description": "Accepted update request. Empty response body. (For asynchronous requests if supported by service features.)"
          }},
          "400": {{
            "description": "Invalid Input",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to update an item in a static collection.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "Not found. The requested collection or member item was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "delete": {{
        "summary": "Remove a collection member item.",
        "description": "Removes a member item from a collection. The response may differ depending upon whether or not the  service features include support for asynchronous actions.",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Persistent identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member",
            "required": true
          }}
        ],
        "tags": [
          "Members"
        ],
        "security": [
          {{
            "oauth": [
              "write"
            ]
          }}
        ],
        "responses": {{
          "200": {{
            "description": "Successful removal. Empty response body."
          }},
          "202": {{
            "description": "Accepted request. Empty response body. (For asynchronous requests, if supported by service features.)"
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to remove  item from a static collection."
          }},
          "404": {{
            "description": "Not Found",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "default": {{
            "description": "Unexpected error",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }},
    "/collections/{{id}}/members/{{mid}}/properties/{{property}}": {{
      "get": {{
        "summary": "Get a named property of a member item in a collection",
        "description": "This request retrieves a specific named property of a specific member item from a collection",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member item.",
            "required": true
          }},
          {{
            "name": "property",
            "in": "path",
            "type": "string",
            "description": "the name of a property to retrieve (e.g. index)",
            "required": true
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "200": {{
            "description": "The requested member",
            "schema": {{
              "$ref": "#/definitions/MemberItem"
            }}
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "404": {{
            "description": "Not found. The requested collection or member item was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "put": {{
        "summary": "Update a named property of a member item in a collection",
        "description": "This request updates a specific named property of a specific member item from a collection",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member item.",
            "required": true
          }},
          {{
            "name": "property",
            "in": "path",
            "type": "string",
            "description": "the name of a property to update",
            "required": true
          }},
          {{
            "name": "content",
            "in": "body",
            "description": "new property value",
            "required": true,
            "schema": {{
              "type": "string"
            }}
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "200": {{
            "description": "Successful update. The updated member item is returned in the response.",
            "schema": {{
              "$ref": "#/definitions/MemberItem"
            }}
          }},
          "202": {{
            "description": "Accepted update request. Empty response body. (For asynchronous requests, if supported by service features.)"
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to update a static item."
          }},
          "404": {{
            "description": "Not found. The requested collection or member item was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }},
      "delete": {{
        "summary": "Delete a named property of a member item in a collection",
        "description": "This request deletes a specific named property of a specific member item from a collection",
        "parameters": [
          {{
            "name": "id",
            "in": "path",
            "description": "Identifier for the collection",
            "required": true,
            "type": "string"
          }},
          {{
            "name": "mid",
            "in": "path",
            "type": "string",
            "description": "Identifier for the collection member item.",
            "required": true
          }},
          {{
            "name": "property",
            "in": "path",
            "type": "string",
            "description": "the name of a property to update",
            "required": true
          }}
        ],
        "tags": [
          "Members"
        ],
        "responses": {{
          "200": {{
            "description": "Successful deletion. Empty response body."
          }},
          "202": {{
            "description": "Accepted delete request. Empty response body. (For asyncrhonous requests, if supported by service features.)"
          }},
          "401": {{
            "description": "Unauthorized. Request was not authorized.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }},
          "403": {{
            "description": "Forbidden. May be returned, for example, if a request was made to delete a required metadata property or update a static item."
          }},
          "404": {{
            "description": "Not found. The requested collection or member item was not found.",
            "schema": {{
              "$ref": "#/definitions/Error"
            }}
          }}
        }}
      }}
    }}
  }},
  "definitions": {{
    "CollectionCapabilities": {{
      "description": "Capabilities define the set of actions that are supported by a collection.",
      "type": "object",
      "required": [
        "isOrdered",
        "appendsToEnd",
        "supportsRoles",
        "membershipIsMutable",
        "propertiesAreMutable",
        "restrictedToType",
        "maxLength"
      ],
      "properties": {{
        "isOrdered": {{
          "type": "boolean",
          "description": "Identifies whether the collection items are kept in a consistent, meaningful order. The exact nature of the ordering is not specified, but see also appendsToEnd property.",
          "default": false
        }},
        "appendsToEnd": {{
          "type": "boolean",
          "description": "For an ordered collection, indicates that new items are appended to the end rather than insertable at a specified, possibly invalid, index points. Only valid if isOrdered is true.",
          "default": true
        }},
        "supportsRoles": {{
          "type": "boolean",
          "description": "Indicates whether the collection supports assigning roles to its member items. Available roles are determined by the Collection Model type.",
          "default": false
        }},
        "membershipIsMutable": {{
          "type": "boolean",
          "description": "Indicates whether collection membership mutable (i.e. whether members can be added and removed)",
          "default": true
        }},
        "propertiesAreMutable": {{
          "type": "boolean",
          "description": "Indicates whether collection properties are mutable (i.e. can the metadata of this collection be changed)",
          "default": true
        }},
        "restrictedToType": {{
          "type": "string",
          "description": "If specified, indicates that the collection is made up of homogenous items of the specified type. Type should be specified using the PID of a registered Data Type or a controlled vocabulary."
        }},
        "maxLength": {{
          "type": "integer",
          "description": "The maximum length of the Collection. -1 means length is not restricted.",
          "default": -1
        }}
      }}
    }},
    "MemberItem": {{
      "description": "A member item in a collection",
      "type": "object",
      "required": [
        "id",
        "location"
      ],
      "properties": {{
        "id": {{
          "type": "string",
          "description": "Identifier for the member"
        }},
        "location": {{
          "type": "string",
          "description": "Location at which the item data can be retrieved"
        }},
        "description": {{
          "type": "string",
          "description": "Human readable description"
        }},
        "datatype": {{
          "type": "string",
          "description": "URI of the data type of this item"
        }},
        "ontology": {{
          "type": "string",
          "description": "URI of an ontology model class that applies to this item"
        }},
        "mappings": {{
          "$ref": "#/definitions/CollectionItemMappingMetadata"
        }}
      }}
    }},
    "CollectionProperties": {{
      "description": "Functional Properties of the Collection",
      "type": "object",
      "required": [
        "dateCreated",
        "ownership",
        "license",
        "modelType",
        "hasAccessRestrictions",
        "descriptionOntology"
      ],
      "properties": {{
        "dateCreated": {{
          "type": "string",
          "format": "date-time",
          "description": "The date the collection was created."
        }},
        "ownership": {{
          "type": "string",
          "description": "Indicates the owner of the Collection. Implementation is expected to use a controlled vocabulary or PIDs."
        }},
        "license": {{
          "type": "string",
          "description": "Indicates the license that applies to the Collection. Implementation is expected to use a controlled vocabulary, stable URIs or PIDs of registered data types. "
        }},
        "modelType": {{
          "type": "string",
          "description": "Identifies the model that the collection adheres to. Iimplementation is expected to use a controlled vocabulary, or PIDs of registered data types. "
        }},
        "hasAccessRestrictions": {{
          "type": "boolean",
          "description": "Indicates whether the collection is fully open or has access restrictions. ",
          "default": false
        }},
        "memberOf": {{
          "type": "array",
          "description": "If provided, this is a list of collection identifiers to which this collection itself belongs. This property is only meaningful if the service features supports a  maximumExpansionDepth > 0.",
          "items": {{
            "type": "string"
          }},
          "default": []
        }},
        "descriptionOntology": {{
          "type": "string",
          "description": "Identifies the ontology used for descriptive metadata. Implementation is expected to supply the URI of a controlled vocabulary."
        }}
      }}
    }},
    "CollectionObject": {{
      "description": "Defines the schema for a collection object.",
      "type": "object",
      "required": [
        "id",
        "capabilities",
        "properties"
      ],
      "properties": {{
        "id": {{
          "type": "string",
          "description": "Identifier for the collection. This is ideally a PID."
        }},
        "capabilities": {{
          "$ref": "#/definitions/CollectionCapabilities"
        }},
        "properties": {{
          "$ref": "#/definitions/CollectionProperties"
        }},
        "description": {{
          "type": "object",
          "description": "Descriptive metadata about the collection.  The properties available for this object are dependent upon the description ontology used, as define in the collection properties."
        }}
      }}
    }},
    "CollectionResultSet": {{
      "description": "A resultset containing a potentially iterable list of Collections Objects. This is the  schema for the response to any request which retrieves collection items.",
      "type": "object",
      "required": [
        "contents"
      ],
      "properties": {{
        "contents": {{
          "type": "array",
          "description": "list of Collection Objects returned in response to a query",
          "items": {{
            "$ref": "#/definitions/CollectionObject"
          }}
        }},
        "next_cursor": {{
          "type": "string",
          "description": "If the service supports pagination, and the resultset is paginated, this will be a cursor which can be used to retrieve the next page in the results."
        }},
        "prev_cursor": {{
          "type": "string",
          "description": "If the service supports pagination, and the resultset is paginated, this will be a cursor which can be used to retrieve the next page in the results."
        }}
      }}
    }},
    "MemberResultSet": {{
      "description": "A resultset containing a potentially iterable list of Member Items. This is the schema for the response to any request which retrieves collection members.",
      "type": "object",
      "required": [
        "contents"
      ],
      "properties": {{
        "contents": {{
          "type": "array",
          "description": "list of Member Items returned in responses to a query",
          "items": {{
            "$ref": "#/definitions/MemberItem"
          }}
        }},
        "next_cursor": {{
          "type": "string",
          "description": "If the service supports pagination, and the resultset is paginated, this will be cursor which can be used to retrieve the next page in the results."
        }},
        "prev_cursor": {{
          "type": "string",
          "description": "If the service supports pagination, and the resultset is paginated, this will be cursor which can be used to retrieve the next page in the results."
        }}
      }}
    }},
    "Error": {{
      "type": "object",
      "description": "A error response object",
      "properties": {{
        "code": {{
          "type": "integer",
          "format": "int32",
          "description": "error code"
        }},
        "message": {{
          "type": "string",
          "description": "error message"
        }}
      }}
    }},
    "ServiceFeatures": {{
      "description": "Describes the properties of the response to the Service /features request.",
      "type": "object",
      "required": [
        "providesCollectionPids",
        "enforcesAccess",
        "supportsPagination",
        "asynchronousActions",
        "ruleBasedGeneration",
        "maxExpansionDepth",
        "providesVersioning",
        "supportedCollectionOperations",
        "supportedModelTypes"
      ],
      "properties": {{
        "providesCollectionPids": {{
          "type": "boolean",
          "description": "Indicates whether this services provides collection PIDs for new collections. If this is false, requests for new Collections must supply the PID for the collection. If this is true, the Service will use its default PID provider (as advertised via the collectionPidProviderType feature) to create new PIDs to assign to new Collections.",
          "default": false
        }},
        "collectionPidProviderType": {{
          "type": "string",
          "description": "Identifies the PID provider service used by the Collection Service to create new PIDs for new Collection. Required if providesCollectionPids is true, otherwise this property is optional and has no meaning. Recommended to use a Controlled Vocabulary or registered Data Types"
        }},
        "enforcesAccess": {{
          "type": "boolean",
          "description": "Indicates whether or not the service enforces access controls on requests. Implementation details access are left up to the implementor. This flag simply states whether or not the Service enforces access.",
          "default": false
        }},
        "supportsPagination": {{
          "type": "boolean",
          "description": "Indicates whether or not the service offers pagination (via cursors) of response data.",
          "default": false
        }},
        "asynchronousActions": {{
          "type": "boolean",
          "description": "Indicates whether or not actions such as update, delete occur synchronously or may be queued for later action.",
          "default": false
        }},
        "ruleBasedGeneration": {{
          "type": "boolean",
          "description": "Indicates whether or not the service allows rule-based generation of new collections."
        }},
        "maxExpansionDepth": {{
          "type": "integer",
          "description": "The maximum depth to which collection members can be expanded. A value of 0 means that expansion is not supppoted. A value of -1 means that the collections can be expanded to infinite depth.",
          "default": 0
        }},
        "providesVersioning": {{
          "type": "boolean",
          "description": "Indicates whether the service offers support for versioning of Collections. Implementation details are left up to the implementor.",
          "default": false
        }},
        "supportedCollectionOperations": {{
          "type": "array",
          "items": [
            {{
              "$ref": "#/definitions/CollectionOperations"
            }}
          ],
          "description": "List of collection-level set operations that are supported by this service.",
          "default": []
        }},
        "supportedModelTypes": {{
          "type": "array",
          "items": [
            {{
              "type": "string"
            }}
          ],
          "description": "List of collection model types supported by this service.  Recommended to use a Controlled Vocabulary or registered Data Types",
          "default": []
        }}
      }}
    }},
    "CollectionOperations": {{
      "description": "Valid operation names.",
      "type": "string",
      "enum": [
        "findMatch",
        "intersection",
        "union",
        "flatten"
      ]
    }},
    "CollectionItemMappingMetadata": {{
      "description": "metadata on an item which is available by mapping from capabilities",
      "type": "object",
      "properties": {{
        "role": {{
          "type": "string",
          "description": "The ole that applies to this item. Only available if the collection supportsRoles per its capabilities. A Controlled Vocabulary should be used."
        }},
        "index": {{
          "type": "integer",
          "description": "position of the item in the collection. Only available if the Collection isOrdered per its capabilities."
        }},
        "dateAdded": {{
          "type": "string",
          "format": "date-time",
          "description": "The date the item was added to the collection."
        }},
        "dateUpdated": {{
          "type": "string",
          "format": "date-time",
          "description": "The date the item's metadata were last updated."
        }}
      }}
    }}
  }}
}}""".format((',').join(["\""+s+"\"" for s in schemes]), host, port, base_path).encode()