# HTTP Status Codes Reference

## Successful Responses
HTTP 200 OK indicates a successful request. HTTP 201 Created indicates that a resource was created. HTTP 204 No Content indicates success without a response body.

## Client Errors
HTTP 400 Bad Request indicates invalid request data. HTTP 401 Unauthorized indicates missing or invalid authentication. HTTP 403 Forbidden means the server refuses access.

## Server Errors
HTTP 500 Internal Server Error indicates an unexpected server-side failure. HTTP 502 Bad Gateway indicates an invalid response from an upstream server. HTTP 503 Service Unavailable means the service is temporarily unable to handle the request.

## Debugging
Inspect the response status code, response body, request URL, HTTP method, and server logs. Match the status code to the relevant troubleshooting guide before changing application code.
