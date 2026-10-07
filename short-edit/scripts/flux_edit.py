import base64, json, os, sys, time, urllib.request
T = os.environ["REPLICATE_API_TOKEN"]; H = {"Authorization": f"Bearer {T}", "Content-Type": "application/json", "User-Agent": "curl/8.7.1"}
def api(m, u, b=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, method=m, data=json.dumps(b).encode() if b else None, headers=H), timeout=180))
def uri(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
frame, ref, out, prompt = sys.argv[1:5]
model = sys.argv[5] if len(sys.argv) > 5 else "flux-2-max"
inp = ({"prompt": prompt, "images": [uri(frame), uri(ref)], "aspect_ratio": "1:1", "resolution": "2k", "grounding": False,
        "output_format": "png", "safety_tolerance": 2} if model == "flux-3-image" else
       {"prompt": prompt, "input_images": [uri(frame), uri(ref)], "aspect_ratio": "1:1", "resolution": "4 MP",
        "output_format": "png", "safety_tolerance": 2})
p = api("POST", f"https://api.replicate.com/v1/models/black-forest-labs/{model}/predictions", {"input": inp})
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(2); p = api("GET", p["urls"]["get"])
if p["status"] != "succeeded":
    sys.exit(f"{p['status']}: {p.get('error')}")
o = p["output"] if isinstance(p["output"], str) else p["output"][0]
open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(o, headers={"User-Agent": "curl/8.7.1"}), timeout=180).read())
print(out)
