import argparse

from .client import Gateway
from .models import PromptRequest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--stream", action="store_true")
    a = ap.parse_args()
    gw, req = Gateway(), PromptRequest(prompt=a.prompt)
    if a.stream:
        for chunk in gw.stream(req):
            print(chunk, end="", flush=True)
        print()
    else:
        out = gw.invoke(req)
        print(out.text)
        print(
            f"[{out.model_id} in={out.input_tokens} out={out.output_tokens} {out.latency_ms}ms]"
        )


if __name__ == "__main__":
    main()
