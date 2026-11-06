Verification before sign-in
========================================================================

Status: proposed, pending review. This contributor proposal is excluded from the
published documentation. It is not a user manual or a description of the system.

Tracking: `docs #81 <https://github.com/PapyrusReader/docs/issues/81>`_.
Implementation: `server #22 <https://github.com/PapyrusReader/server/issues/22>`_
and `client #60 <https://github.com/PapyrusReader/client/issues/60>`_.

This is the proposed HTTP contract for ``TASK-AUTH-01``, implementing the
verification portions of ``FR-1_1``, ``FR-1_2`` and ``FR-1_3``.
It becomes the implementation baseline when this documentation change is merged.
It is not a description of deployed behavior. Server and client delivery remain
``TASK-AUTH-02`` and ``TASK-AUTH-03``. Password policy, password recovery
policy, account deletion policy and full-library search are outside this change.

Source review on 2026-11-06 used server revision
``c71a82cb70a62f0f5ded5330827aa1cdebee737c`` and client revision
``3a3f6b5c1cffc33930dcfdf956ac272fbb007f1c``. Registration currently creates an
unverified user and immediately issues tokens. Login, refresh and the API session
dependency do not check verification. Verification/resend services already exist,
but registration does not send their email. The client parses registration as
``AuthTokens`` and saves those tokens immediately. The Google identity model
does not retain the hosted-domain claim needed for the authority decision below.

Invariants and response types
------------------------------------------------------------------------

Examples use the default ``/v1`` API prefix. Clients must use their configured
``PapyrusApiConfig`` prefix, never hardcode it. Requests and responses use JSON.
Auth responses use ``Cache-Control: no-store``. Secrets, verification links and
OAuth codes must not appear in application logs or analytics.

An account is eligible for application access only when its current primary
email has accepted verification evidence and the account is otherwise active.
Neither a pending account nor a verification token is an authenticated session.
No pending response contains ``access_token``, ``refresh_token``, a PowerSync
credential or a library-access capability. Verification itself never signs in.
After verification the user repeats password or Google sign-in.

Successful login, Google exchange and refresh retain the existing ``AuthTokens``
shape and HTTP 200. No new discriminator is required for successful tokens:

.. code-block:: json

   {
     "access_token": "<short-lived-api-jwt>",
     "refresh_token": "<opaque-refresh-token>",
     "token_type": "Bearer",
     "expires_in": 3600,
     "user": {
       "user_id": "00000000-0000-4000-8000-000000000001",
       "email": "reader@example.com",
       "display_name": "Reader",
       "avatar_url": null,
       "email_verified": true,
       "created_at": "2026-11-06T10:00:00Z",
       "last_login_at": "2026-11-06T10:10:00Z",
       "connected_providers": []
     }
   }

The example expiry is illustrative. Configured token lifetimes remain unchanged.
Refresh rotation and session revocation remain mandatory. PowerSync credentials
remain separate short-lived tokens issued by ``POST /auth/powersync-token``.

Registration
------------------------------------------------------------------------

``POST /v1/auth/register`` keeps ``RegisterRequest`` unchanged:

.. code-block:: json

   {
     "email": "reader@example.com",
     "password": "<user-entered-password>",
     "display_name": "Reader",
     "client_type": "mobile",
     "device_label": "Reader's phone"
   }

``client_type`` and ``device_label`` remain optional with existing defaults and
validation. They do not create a session or device registration at this stage.
HTTP 201 returns a new ``PendingVerificationResponse``:

.. code-block:: json

   {
     "status": "verification_required",
     "email": "reader@example.com",
     "message": "Check your email to verify your account, then sign in.",
     "resend_after": 60
   }

``email`` is the normalized submitted address. ``resend_after`` is a nonnegative
integer in seconds. A 201 means the pending account, password hash, verification
token and durable email-delivery job were committed together. It does not mean
SMTP delivery has completed. No ``AuthSession`` row is created.

An existing email returns HTTP 409 ``CONFLICT`` with the existing message
``An account with this email already exists`` and empty details, whether pending
or verified. Never replace its password, name or provider links. After an
ambiguous network failure, the client offers sign-in and resend rather than
assuming registration failed. This deliberately retains the existing registration
enumeration behavior. Resend must not disclose the account's existence or state.

Password login and refresh
------------------------------------------------------------------------

``POST /v1/auth/login`` keeps the existing request:

.. code-block:: json

   {"email": "reader@example.com", "password": "<password>", "client_type": "web"}

Check credentials before disclosing verification state. Wrong passwords, missing
accounts and accounts without a password credential return HTTP 401
``UNAUTHORIZED`` with ``Invalid email or password``. Valid credentials for an
active, unverified account return HTTP 403:

.. code-block:: json

   {
     "error": {
       "code": "EMAIL_VERIFICATION_REQUIRED",
       "message": "Verify your email address before signing in.",
       "details": {"email": "reader@example.com", "resend_after": 0}
     }
   }

The details contain the verified credential owner's current email and remaining
resend cooldown. Login itself does not send email. The client offers resend,
sign-in after verification, and return to the guest library. Correct credentials
for an eligible account return HTTP 200 with ``AuthTokens``.

``POST /v1/auth/refresh`` keeps ``{"refresh_token": "<opaque-token>"}``.
An eligible session returns HTTP 200 with rotated ``AuthTokens``. Missing,
expired, revoked or unknown credentials return HTTP 401 ``UNAUTHORIZED``.
A still-valid legacy session belonging to a now-ineligible unverified account
returns the same HTTP 403 envelope, revokes that account's application sessions
and commits the revocation. It must not rotate or issue tokens. Later retries
with a revoked token return 401. A failed response must not roll back revocation.

Apply the same eligibility check in the shared API session dependency, including
media, sync uploads and PowerSync credential issuance, so existing API JWTs cannot
bypass the refresh check. Preserve credential validity and disabled/deletion
checks before ordinary access. Logout may revoke an otherwise valid unverified
session without granting access to other endpoints.
Session creation, refresh, verification and recovery must serialize their account
state checks with deletion using the existing owner-before-credential lock order.
No concurrent request may mint a session from verification evidence invalidated
by another committed transition.

Resend, delivery and verification links
------------------------------------------------------------------------

``POST /v1/auth/resend-verification`` remains unauthenticated and accepts
``{"email": "reader@example.com"}``. HTTP 200 uses:

.. code-block:: json

   {
     "message": "If the email is registered, a verification link has been sent",
     "resend_after": 60
   }

The existing message is retained for compatibility and means accepted for
delivery, not confirmed inbox delivery. Return the same body for unknown,
verified, administratively disabled and pending addresses. Only an eligible
pending address queues email. Suppress requests within the recipient cooldown
without revealing that suppression or resetting the cooldown.

Registration and resend share a persisted, normalized-recipient cooldown of
60 seconds, enforced across workers. Apply it to automatic Google verification
mail as well. Public attempts also have an IP limit of at most five requests per
minute per auth endpoint, including password login. A stricter configured limit
is allowed. Per-IP throttling applies before account lookup and returns HTTP 429
``RATE_LIMIT_EXCEEDED``, ``Retry-After`` seconds, and matching
``error.details.retry_after``. Recipient suppression still returns generic 200.

Verification tokens are opaque, hashed for lookup, bound to the user and exact
normalized primary email, single-use and valid for 24 hours from issue. Resend
does not invalidate another unexpired link, avoiding denial of service through
unsolicited resend. Successful verification consumes all outstanding verification
tokens for that address and cancels its pending verification deliveries. Changing
the primary email invalidates old evidence and tokens. Duplicate delivery of the
same email must not extend validity.

Use a dedicated verification-delivery job or an explicitly typed extension of the
existing transactional notification queue. The existing account-deletion notices
are not verification messages and must keep their own ordering and retention.
Commit token and delivery job atomically, retry transient SMTP failures with
backoff, and expire the job no later than its token. A queued job necessarily
contains the deliverable secret, unlike the hashed lookup row. Restrict access,
exclude it from logs, and remove it after delivery, expiry, verification or
account deletion. Do not queue raw passwords. SMTP failure after commit leaves
the account pending and permits resend after the cooldown.

If delivery or the verification landing URL is not configured, return HTTP 503
``VERIFICATION_UNAVAILABLE`` with message
``Verification email is temporarily unavailable. Please try again later.``, empty details and
``Retry-After: 60``. For resend this server-wide check precedes account lookup
and applies equally to all addresses. Registration must not commit a new account
in this state. Queue/transaction failures also return 503 and roll back account,
token and job changes. An unknown commit outcome is handled through sign-in or
resend, never by overwriting a pending account.

Email links target the configured app base URL at
``/verify-email?token=<opaque-token>``. The client route is new. It must support
direct loading while signed out, expired-link guidance and token submission to
the configured API. A GET only displays a confirmation action, so mail scanners
do not consume the link. Explicit confirmation calls
``POST /v1/auth/verify-email`` with ``{"token": "<opaque-token>"}``.
Remove the token from visible history after capture and use a no-referrer policy
on the landing page. Do not load third-party resources with the token in the URL.
Links must resolve to the same deployment as the issuing server. A mismatch must
not switch profiles or transmit the token to another configured server.

HTTP 200 retains ``{"message": "Email verified successfully"}``. It updates only
verification evidence, without setting tokens, moving libraries, cancelling
deletion or signing in on any device. HTTP 400 uses the same public code and
message for expired, malformed, unknown, reused and wrong-address tokens:

.. code-block:: json

   {
     "error": {
       "code": "VERIFICATION_TOKEN_INVALID",
       "message": "This verification link is invalid or expired. Request a new link or sign in if you already verified.",
       "details": {}
     }
   }

Serialize consumption and account state checks so only one concurrent request
succeeds. After a lost success response, the client can try signing in or request
another link. A replay does not produce credentials or reveal the account.

Google sign-in and exchange
------------------------------------------------------------------------

Keep the existing ``GET /auth/oauth/google/start?redirect_uri=...``, validated
state, redirect allowlist, ``GET /auth/oauth/google/callback`` and HTTP 302
handoff to the platform callback with ``?code=<one-time-code>``. Do not put email,
access tokens or verification tokens in that callback URL. Cancellation and
provider errors continue through the callback's ``error`` parameter without a
profile switch. Invalid state is rejected before any redirect or account write.

Validate the Google ID token signature, issuer, audience and expiry. Identify the
Google account by ``sub``, never by email. Under
`Google's email-ownership guidance
<https://developers.google.com/identity/sign-in/android/backend-auth>`_, Gmail
addresses establish Google authority, while Workspace requires
``email_verified=true`` and a nonempty signed ``hd`` claim. An email domain string
alone is not Workspace evidence. Other addresses require Papyrus verification,
even when Google reports ``email_verified=true``. Retain the validated hosted
domain in the internal identity/evidence model, not just the current boolean.

New users get no session in the callback. For non-authoritative addresses, create
a pending account and queue its Papyrus verification email transactionally.
When an existing linked account still needs verification, queue mail subject to
the same recipient cooldown. An already queued delivery need not be duplicated.
An existing linked subject keeps its user ID and library. Never silently replace
its primary email with a changed provider address or downgrade independent
Papyrus verification. Authority for a provider email only establishes eligibility
when that email matches the primary address being verified. For an existing
linked subject with no primary address, bind the supplied email only if it is
not owned by another account, then apply the same verification rule. A different
subject matching an existing email continues
to receive ``account_exists`` and must prove control of that account before
linking. A new Google account without an email receives callback
``error=email_required`` without an account or session. The UI explains that
an email address is required and offers email registration.
For a legacy linked account that still has no primary or provider email, preserve
its user ID and data and return the same error with guidance to contact the server
operator. Do not silently create a replacement account. Account email editing is
outside this task.

``POST /v1/auth/exchange-code`` keeps this request:

.. code-block:: json

   {"code": "<one-time-code>", "client_type": "desktop", "device_label": "Laptop"}

An eligible account receives HTTP 200 with ``AuthTokens``. An unverified account
receives HTTP 403 ``EMAIL_VERIFICATION_REQUIRED`` with the same details as login.
The code is consumed and that consumption committed for either outcome. No
session is created for the latter. Verification mail already queued by the
callback is not duplicated by exchange. If delivery is unavailable for a pending
flow, the callback returns ``error=verification_unavailable`` without creating a
new account or handoff code. An existing pending account remains available for
resend. Verified Google sign-in must still work during an SMTP outage.

An invalid, expired, reused or wrong-purpose exchange code returns HTTP 401
``UNAUTHORIZED`` and grants nothing. After email verification, restart Google
sign-in to obtain a fresh code. Never promote a stale pending code into a session.
The callback must bind the handoff to its eligibility outcome, and exchange must
recheck current account eligibility before granting access. Use the existing
``AuthExchangeCode.purpose`` field with ``login`` for an eligible callback and
``login_pending_verification`` for a pending callback. Exchange accepts these two
purposes only. A pending-purpose code always returns 403, even if verification
finishes before exchange, and the client then repeats Google sign-in.
Linking and account
deletion use separate code purposes and cannot use a login code as authorization.

Errors and existing account lifecycle
------------------------------------------------------------------------

New application errors use the existing
``{"error": {"code": "...", "message": "...", "details": {}}}`` envelope.
Clients branch on codes and fields, not English messages. In addition to the
endpoint-specific outcomes above, schema validation retains HTTP 422 and its
existing FastAPI ``detail`` array. Rate limiting uses the existing 429 envelope.
No failure response includes application tokens.

Disabled accounts remain forbidden. Sign-in to a recoverable deleted account
continues to return the existing ``ACCOUNT_DELETION_PENDING`` authorization after
valid credentials, without ordinary access. Preserve explicit recovery and its
deadline. Add the shared verification guard before recovery can issue a session:
for an unverified account ``/account-deletion/cancel`` returns
``EMAIL_VERIFICATION_REQUIRED`` without consuming recovery authorization or
cancelling deletion. Verification and resend may operate during the recovery
window, but never after permanent deletion or administrative disablement.
The user then signs in again and explicitly recovers. Verification alone must
not clear ``disabled_at`` or any deletion fields. This closes an alternate token
issuance path without changing the deletion policy.

Client state and existing data
------------------------------------------------------------------------

Parse registration's pending result separately from ``AuthTokens``. Parse the
403 details into a pending-verification state in ``AuthApiException`` and the
provider. Keep only the server-scoped email and cooldown needed for guidance.
Do not save passwords, verification tokens or handoff codes for later sign-in.
Reject malformed responses and token responses with ``email_verified=false``
before saving tokens or installing an account profile.

Registration, resend, verification, cancellation and provider errors do not change
the active library. Guest records are never merged, copied or uploaded. Only a
successful eligible sign-in invokes the existing profile-switch queue. On denied
refresh, stop sync and clear credentials while retaining account-scoped local
books, media, positions and queued writes. Keep those writes in their original
profile, available for reconnection after verification. An unrelated account or
server must never acquire them. Guest access remains available. Offline cached
reading is not itself a new server session and must remain usable.

Existing verified users keep their identity, password, library and valid sessions
when their verification evidence is trustworthy. The current boolean conflates
Papyrus verification and Google claims, so migration cannot simply trust all
true values or reset all users. Add durable evidence bound to the verified email
and source (Papyrus email link or authoritative Google identity). Backfill only
where retained records establish that evidence. Password-only accounts marked
verified by the existing email flow can retain it. For Google-linked accounts
without attributable evidence, require a fresh authoritative Google sign-in or
Papyrus link, preserving all data. Do not infer Workspace authority from a stored
domain or ``email_verified_at_provider``. Record the affected account count and
the exact migration predicate in the server PR before activation.

Implementation map and acceptance
------------------------------------------------------------------------

Paths below are relative to the Papyrus workspace. They identify the current
owners and required changes, not code delivered by this document.

.. list-table::
   :header-rows: 1
   :widths: 42 58

   * - Owner
     - Changes and focused evidence
   * - ``server/papyrus/schemas/auth.py``, ``api/routes/auth.py``
     - Add pending response and explicit errors. Preserve successful tokens,
       request fields and configurable prefix. Export OpenAPI after implementation.
       Update ``core/exceptions.py`` and ``main.py`` for the new error codes,
       ``Retry-After`` and no-store headers, including dependency failures.
   * - ``server/papyrus/services/auth/{sessions,email_flows,google,_core,types}.py``
     - Enforce eligibility, retain Google authority evidence, consume handoffs,
       bind verification tokens to email, serialize retries and revocation.
   * - ``server/papyrus/api/deps.py``, ``services/account_deletion.py``
     - Guard existing access JWTs, PowerSync issuance and recovery without changing
       deletion policy. Keep logout available for revocation.
   * - ``server/papyrus/models/{auth,user}.py``, ``alembic/versions/``,
       ``services/account_notifications.py``, ``services/auth/email_flows.py``,
       ``core/rate_limit.py``, ``config.py``
     - Add evidence, address binding, recipient cooldown and durable verification
       delivery. Preserve existing notice behavior and data. Document migration.
   * - ``client/app/lib/auth/{auth_models,auth_api_client,auth_repository}.dart``,
       ``providers/auth_provider.dart``
     - Parse pending/error outcomes before token persistence. Preserve refresh,
       logout, account recovery, cancellation and server/profile isolation.
   * - ``client/app/lib/pages/{register_page,login_page}.dart``,
       ``pages/auth/{actions,oauth_callback_page}.dart``, ``config/app_router.dart``
     - Add verification guidance and cold-loadable ``/verify-email`` route,
       resend cooldown, invalid-link/retry states and existing platform callbacks.
   * - ``server/tests/api/routes/test_auth.py``, ``tests/services/test_auth.py``,
       ``tests/api/routes/test_account_deletion.py``, ``tests/services/test_account_deletion.py``
     - Verify no session for pending accounts, old JWT rejection, refresh revocation,
       all Google authority cases, recovery guard, expired/reused/concurrent tokens,
       delivery failures and migration preservation using a distinct test database.
   * - ``client/app/test/auth/{auth_api_client_test,auth_repository_powersync_test,auth_repository_account_deletion_test,token_store_test}.dart``,
       ``test/providers/auth_provider_test.dart``, ``test/widgets/auth/``,
       ``test/powersync/sync_profile_switch_queue_test.dart``
     - Prove pending outcomes never save tokens or activate profiles. Cover retries,
       cancellation, reload, server changes, guest isolation and preserved offline
       queues. Add focused landing-page and notification-queue regressions.

The server task must also cover unknown/verified/pending resend responses,
cross-worker cooldowns, atomic queue failure, delayed SMTP delivery, token/email
mismatch and legitimate verified-user regression cases. Google provider tests
may use validated-claim fixtures. Real provider smoke tests remain opt-in.

Run ``tools/papyrus check server`` and the focused auth, recovery and migration
tests against a distinct test database. Run ``tools/papyrus check client`` and
the focused auth/provider/widget tests for the client task. Database test runs
must not overlap on the same test database.

The client task must supply narrow-mobile and desktop layout evidence plus web
compilation, with actual callback checks for the available web, desktop and
mobile targets. Record unrun devices explicitly. A browser build does not prove
native deep links. The API prefix and nondefault self-hosted app base path belong
in callback/verification-link tests.

Rollout and rollback
------------------------------------------------------------------------

1. Merge this contract first. Keep the product requirements partial until their
   behavior is implemented and accepted. Do not change the committed OpenAPI
   snapshot to pretend these proposed responses already exist.
   After merge, record acceptance for #81 and synchronize the project from the
   committed docs revision before launching the dependent server task. Review
   any ``spec-changed`` markers deliberately rather than bypassing task gates.
2. Implement and review the server task against this contract, including its
   additive migration and data audit. Validate in staging with the client task.
   Server implementation precedes client integration, but production deployment
   need not follow that order.
3. Release the compatible client before enforcing the new server behavior. It
   accepts existing successful ``AuthTokens`` only for verified users, as well as
   new pending responses. On an old server's unverified token response it saves
   nothing, attempts revocation with the returned access token and offers resend.
   Deploy the web verification landing route and confirm the public app URL and
   email transport before server cutover. Native users may verify in the web app
   and then repeat sign-in in the native app.
4. Apply the migration and deploy the enforcing server through the normal
   ``development`` to ``master`` release process. The server must enforce the
   rule for every client version, without a legacy-client bypass. Older clients
   can still sign in as verified users using unchanged token responses. They may
   not understand pending registration and must update to use the new guidance.
   Registration on an old client still creates only a pending account and sends
   email. Repeating registration does not replace it.
5. Revoke ineligible legacy sessions and reject their existing API JWTs. Previously
   issued PowerSync JWTs can survive until expiry (currently five minutes by
   default). Deny renewal and wait the actual configured lifetime before claiming
   complete removal of live sync access. Cached offline files remain local.
6. Refresh the OpenAPI snapshot from the accepted server revision and record
   endpoint, mail, profile-isolation and platform evidence. Close implementation
   tasks only after their own acceptance, independently of this contract PR.

Rollback must retain verification enforcement, evidence and pending accounts.
Do not downgrade to a server that grants unverified sessions or reverse the
migration by deleting user data. If the enforcing release cannot serve auth,
temporarily return a retryable service-unavailable response for affected auth
entry points while preserving offline reading, then fix forward. Record any
temporary outage separately from successful deployment acceptance.
