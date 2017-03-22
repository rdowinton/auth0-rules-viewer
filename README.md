# Auth0 Application Rules Viewer
## Preparing an Auth0 client for the viewer
1. Create SPA client in Auth0.
2. Create a rule for the client to whitelist users. The `Whitelist for a Specific App` sample rule is exactly what you need.
3. In your new client's Settings tab:
  * Add `http://localhost/login` to the Allowed Callback URLs
  * Add `http://localhost` to the Allowed Origins (CORS)

## Preparing an Auth0 client for the management API
1. Create a non-interactive client.
2. Authorize the non-interactive client you created in Auth0 Management API's Non Interactive Clients section.
3. Authorize the non-interactive client for Auth0 management API.

## Configuring locally
1. Set your SPA client's ID and your domain in `frontend/src/views/Main/routes.js`.
2. Set your domain as well as your non-interactive client's `client_id`, `client_secret`, and `audience` in `api/config.py`.
Your token URL is your domain followed by /oauth/token, e.g.: `http://username.eu.auth0.com/oauth/token`.

## Building the viewer
1. Change directory into `rules/frontend`.
2. Install the necessary dependencies from `package.json` via `npm`:
```
$ npm install
```
3. Build:
```
$ npm run build
```

## Running the viewer
1. Start the Docker container with docker-compose:
```
$ docker-compose up
```
2. The viewer will now be running on `http://localhost/`.
