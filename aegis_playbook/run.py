"""aegis_playbook — red-team your Telegram admin bot against a labeled scam playbook.

Usage:
    python -m aegis_playbook.run --regex "(?i)airdrop|claim.*free"        # test a regex
    python -m aegis_playbook.run --target mybot.filter                    # test importable callable
"""
import argparse, importlib, json, os, re, sys, time

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "scam_plays.jsonl")


def load_plays(path=DATA):
    plays = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                plays.append(json.loads(line))
    return plays


def default_detector(text):
    """Naive keyword demo detector — replace with your own bot logic."""
    pats = [
        r"(?i)airdrop", r"(?i)claim.{0,20}free", r"(?i)guarantee\w*\s+(roi|profit|return)",
        r"(?i)seed.?phrase|mnemonic|private\s?key", r"(?i)dm\s+me|contact\s+(me|admin|support)",
        r"(?i)verify.{0,20}wallet|connect.{0,20}wallet", r"(?i)presale|whitelist\s+now",
        r"(?i)double\s+your|2x|10x\s+guarantee", r"(?i)send\s+(eth|btc|usdt|sol)\s+to",
        r"(?i)liquidity.{0,20}(lock|rug)|honeypot",
    ]
    return any(re.search(p, text) for p in pats)


def resolve_target(spec):
    if not spec:
        return default_detector
    mod_name, _, fn_name = spec.partition(":")
    if not fn_name:
        mod_name, _, fn_name = spec.rpartition(".")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, fn_name)
    return fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="module:function callable(text)->bool (True=block). Empty = demo regex detector")
    ap.add_argument("--regex", help="shortcut: test a single regex as the detector")
    ap.add_argument("--data", default=DATA)
    args = ap.parse_args()

    if args.regex:
        rx = re.compile(args.regex)
        detector = lambda text: bool(rx.search(text))
    else:
        detector = resolve_target(args.target)

    plays = load_plays(args.data)
    blocked = missed = fp = 0
    missed_ids, fp_ids = [], []
    t0 = time.time()
    for p in plays:
        hit = bool(detector(p["text"]))
        if p["category"] == "benign_control":
            if hit:
                fp += 1
                fp_ids.append(p["id"])
        elif hit:
            blocked += 1
        else:
            missed += 1
            missed_ids.append(p["id"])
    dt = (time.time() - t0) / max(len(plays), 1) * 1000
    print(f"plays={len(plays)} blocked={blocked} missed={missed} false_positive={fp} "
          f"block_rate={blocked / max(len(plays) - fp, 1):.1%} fp_rate={fp / max(len(plays), 1):.1%} "
          f"avg_latency_ms={dt:.2f}")
    if missed_ids:
        print("missed:", " ".join(missed_ids[:20]))
    if fp_ids:
        print("false_positives:", " ".join(fp_ids))


if __name__ == "__main__":
    main()
