"""
verify_world.py — World ID ZK Proof verification endpoint
Port 5050 — ne touche pas au pipeline 0xDELTA existant
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["*"])

# ── CONFIG ────────────────────────────────────────────────────────────────────
APP_ID    = "app_411ec21928d81bebe5be96beefdf732d"
ACTION_ID = "access-0xdelta-dashboard"
API_KEY   = "0xd36adf37e3545319423f474a8ac69f120b4b272fb61052739051854900625141"

WORLD_VERIFY_URL     = f"https://developer.worldcoin.org/api/v2/verify/{APP_ID}"
VERIFIED_CACHE_FILE  = "/home/classics2323/world_verified.json"
NULLIFIER_TTL        = 86400 * 7  # 7 jours

# ── CACHE ─────────────────────────────────────────────────────────────────────
def load_cache():
    try:
        with open(VERIFIED_CACHE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(VERIFIED_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def is_cached(nullifier):
    cache = load_cache()
    entry = cache.get(nullifier)
    if not entry:
        return False
    return time.time() < entry.get("expires_at", 0)

def cache_nullifier(nullifier, level):
    cache = load_cache()
    cache[nullifier] = {
        "verified_at": int(time.time()),
        "expires_at":  int(time.time()) + NULLIFIER_TTL,
        "level":       level,
        "date":        datetime.now().isoformat()
    }
    save_cache(cache)

# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route("/api/verify-human", methods=["POST"])
def verify_human():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No payload"}), 400

    nullifier = data.get("nullifier_hash", "")
    if not nullifier:
        return jsonify({"success": False, "error": "Missing nullifier_hash"}), 400

    # Cache hit
    if is_cached(nullifier):
        return jsonify({"success": True, "nullifier_hash": nullifier,
                        "access_level": "human", "from_cache": True})

    # Appel World ID API
    try:
        payload = {
            "nullifier_hash":     data.get("nullifier_hash"),
            "merkle_root":        data.get("merkle_root"),
            "proof":              data.get("proof"),
            "verification_level": data.get("verification_level", "orb"),
            "action":             ACTION_ID,
            "signal_hash":        data.get("signal_hash", "0x" + "0" * 64)
        }
        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        resp   = requests.post(WORLD_VERIFY_URL, json=payload, headers=headers, timeout=10)
        result = resp.json()

        if resp.status_code == 200 and result.get("success"):
            level = data.get("verification_level", "orb")
            cache_nullifier(nullifier, level)
            return jsonify({"success": True, "nullifier_hash": nullifier,
                            "access_level": "human", "verification_level": level})
        else:
            return jsonify({"success": False, "error": result.get("code", "unknown"),
                            "detail": result.get("detail", "")}), 400

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "timeout"}), 503
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/human-status", methods=["GET"])
def human_status():
    nullifier = request.args.get("nullifier", "")
    if not nullifier:
        return jsonify({"valid": False}), 400
    return jsonify({"valid": is_cached(nullifier), "nullifier": nullifier})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app_id": APP_ID, "action": ACTION_ID})


if __name__ == "__main__":
    print(f"[0xDELTA] World ID verify endpoint — port 5050")
    app.run(host="0.0.0.0", port=5050, debug=False)
