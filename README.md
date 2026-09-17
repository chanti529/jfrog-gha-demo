# payments-utils-demo

A tiny, working Python package used to demonstrate **JFrog Artifactory + GitHub
Actions build integration** live in Workshop 2.

Nothing about this project is meant to be impressive. That's the point — it's
small enough to read in 30 seconds, so the room's attention stays on the
*pipeline*, not the code.

---

## What's in here

```
jfrog-gha-demo/
├── .github/workflows/build.yml   ← the actual demo — read this first
├── src/payments_utils/
│   ├── __init__.py
│   └── core.py                   ← two small functions (mask + validate a card number)
├── tests/test_core.py            ← 6 unit tests, all passing
├── pyproject.toml
├── requirements.txt
└── README.md
```

`core.py` has two functions: `mask_pan()` masks all but the last 4 digits of a
card number, and `is_valid_card_number()` runs the Luhn checksum. Both are
illustrative only — don't use this for anything real.

---

## Before you run this live

You need a reachable JFrog Platform instance (a free trial or sandbox works
fine) with:

1. **A local repo** named `pypi-local` — where the built package gets published
2. **A remote repo** named `pypi-remote` — proxying `pypi.org`, so `pip
   install` resolves through Artifactory instead of going direct
3. **An access token** (or service account, matching Visa's current pattern)

Then on the GitHub repo hosting this demo:

| Type | Name | Value |
|---|---|---|
| Variable | `JF_URL` | Your JFrog Platform URL |
| Secret | `JF_ACCESS_TOKEN` | The access token from step 3 |

Push to `main`, or trigger manually via **Actions → Build, Test, and Publish
(JFrog Demo) → Run workflow**.

---

## Live Demo Script (~15 min, matches the workshop slot)

### Why (2 min)
Open on the gap from the SDLC slide: *"GitHub Actions builds today leave no
trace in Artifactory. Jenkins does. GH Actions doesn't. That's the blind
spot we're closing right now."*

### What (2 min)
Show `.github/workflows/build.yml` — scroll to the `setup-jfrog-cli@v4` step.
*"One action. That's the entire integration surface. Everything below it is
your normal build — nothing about your existing pipeline changes."*

### How — live run (8 min)
Trigger the workflow (push or manual dispatch). While it runs, narrate each
step against the file:

1. **Checkout + setup Python** — nothing new here
2. **`setup-jfrog-cli@v4`** — authenticates using the `JF_URL` /
   `JF_ACCESS_TOKEN` you set as repo variables/secrets. No token handling
   code, no curl scripts.
3. **`jf pip-config --repo-resolve=pypi-remote`** — this is **take**: pip now
   resolves dependencies through Artifactory instead of public PyPI directly.
4. **Tests run** — same `pytest` command as always.
5. **`jf rt upload`** — this is **give**: the built wheel lands in
   `pypi-local`, tagged with this build's context.
6. **`jf rt build-collect-env` + `jf rt build-publish`** — the build info
   itself gets published: commit SHA, environment, timing, artifacts
   produced.

When the run finishes, open the **Job Summary** on the GitHub Actions run
page — the last step writes a direct link back to the build in Artifactory.
Click it. *"That's the bidirectional link. From here, click through to see
everything this build touched."*

**Backup if wifi is unreliable:** screenshot the GH Actions run summary and
the Artifactory build view ahead of time. Walk through the screenshots in the
same order.

### Benefits (3 min)
Tie back to the give/take slide:
- *"You gave one thing: build info, attached automatically."*
- *"You can now take it back anytime: 'what commit built this artifact?' —
  answered, without asking anyone."*
- *"The 401-ticket pattern goes away too — auth failures here show up in the
  Actions log with the identity and scope, not as a mystery."*

Close with the minimal-effort framing: *"This is one action added to a
workflow you already have. Nobody rewrote their pipeline to get this."*

---

## Same pattern, other ecosystems

**Maven** (for the Java-heavy teams in the room) — same plugin, same shape:

```yaml
- uses: jfrog/setup-jfrog-cli@v4

- name: Build and publish with Maven
  run: |
    jf mvn-config --repo-resolve=maven-remote --repo-deploy=maven-local
    jf mvn clean deploy

- run: jf rt build-publish
```

**Docker** — same shape again:

```yaml
- uses: jfrog/setup-jfrog-cli@v4

- name: Build and push image
  run: |
    jf docker build -t my-registry.jfrog.io/docker-local/my-app:${{ github.sha }} .
    jf docker push my-registry.jfrog.io/docker-local/my-app:${{ github.sha }}

- run: jf rt build-publish
```

Don't build these live unless asked — the Python demo carries the point.
Keep these two snippets on hand only if someone asks "does this work for
Maven / Docker too?"

---

## Local sanity check (already verified working)

```bash
pip install -e .
pip install pytest build
pytest -v          # 6 passed
python -m build    # produces dist/*.whl and dist/*.tar.gz
```
