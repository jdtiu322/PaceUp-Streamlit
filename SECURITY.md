# Security Notes

## Refresh-token cookie

PaceUp currently uses `streamlit_cookies_controller` to store the Firebase refresh token in a browser cookie. The app sets the cookie with `Secure` by default via `AUTH_COOKIE_SECURE=true` and `SameSite=Lax`, but this controller is JavaScript-based and cannot mark the cookie as `HttpOnly`.

Set `AUTH_COOKIE_SECURE=false` only for local HTTP development where secure cookies cannot be written.

That means the refresh token is still exposed to any successful cross-site scripting attack. Treat this as acceptable only for local demos or low-risk prototypes.

For production, replace this with a server-side session:

- Store Firebase refresh tokens only on the server.
- Send the browser an opaque session ID in a `Secure`, `HttpOnly`, `SameSite=Lax` cookie.
- Keep session records in a server-side store such as Firestore, Redis, or the deployment platform's session storage.
- Rotate or revoke server-side sessions on sign-out.
