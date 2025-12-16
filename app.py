import hmac
import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

PORT = 8000
EXPECTED_BEARER = ""  # set to enforce Authorization; empty => skip
EXPECTED_HMAC_SECRET = ""


def bearer_ok(auth_header: str) -> bool:
    if not EXPECTED_BEARER:
        return True
    return hmac.compare_digest(auth_header or "", f"Bearer {EXPECTED_BEARER}")


def hmac_ok(ts: str | None, sig: str | None, id: str | None, raw_body: str) -> bool:
    if not EXPECTED_HMAC_SECRET:
        return True
    if not ts or not sig or not id:
        return False

    # Expect signature header in the format "v1,<hex>"
    version, provided_hex = (sig).split(",", 1)

    if version != "v1":
        return False

    # The signed content is "<id>.<timestamp>.<raw_body>"
    signing = f"{id}.{ts}.{raw_body}".encode("utf-8")
    expected = hmac.new(
        EXPECTED_HMAC_SECRET.encode("utf-8"),
        signing,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest((provided_hex).lower(), expected.lower())


@app.post("/webhook")
def callback():
    raw_body = request.get_data(cache=False, as_text=True) or ""

    try:
        payload = json.loads(raw_body)
    except Exception:
        payload = {}

    auth = request.headers.get("Authorization", "")
    ts = request.headers.get("webhook-timestamp")
    sig = request.headers.get("webhook-signature")
    id = request.headers.get("webhook-id")

    ok = bearer_ok(auth) and hmac_ok(ts, sig, id, raw_body)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return jsonify({"ok": ok}), (200 if ok else 401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
