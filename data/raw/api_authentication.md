# API Authentication and Debugging

## API Keys
An API key identifies or authorizes a client according to the service's policy. Store keys in environment variables or a secret manager rather than hard-coding them in source files.

## Bearer Tokens
A bearer token is commonly sent in the Authorization header using the format Authorization: Bearer followed by the token. Protect tokens because anyone who obtains a valid bearer token may be able to use it.

## Environment Variables
Applications can read configuration from environment variables. A .env file can support local development, but it should not be committed if it contains secrets. Add it to .gitignore and provide a safe example configuration file instead.

## Debugging Requests
Check the endpoint URL, HTTP method, headers, request body, status code, and server logs. A 401 often indicates an authentication problem, while a 403 indicates that the request is not permitted.

## Timeouts and Errors
Set reasonable request timeouts and handle connection errors explicitly. Retry transient failures carefully, using backoff where appropriate, and avoid repeatedly retrying requests that cannot succeed.
