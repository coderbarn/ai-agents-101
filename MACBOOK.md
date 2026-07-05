# Running Codex on an Intel MacBook

Notes for getting Codex running on a MacBook with an Intel Core i7 processor.

## Machine Context

- CPU architecture: Intel / `x86_64`
- Codex platform reported by diagnostics: `macos-x86_64`
- Installed Codex CLI checked with: `codex --version`
- Current local CLI observed: `codex-cli 0.140.0`
- Install location observed: `/usr/local/bin/codex`

## Basic Setup

Install or update Codex with npm:

```bash
npm install -g @openai/codex
```

On this Intel Core i7 MacBook, the version that worked was installed with:

```bash
npm install -g @openai/codex@0.140.0
```

The next step required on this MacBook was to codesign the active Node.js executable with the local entitlements file:

```bash
sudo codesign --force --sign - --entitlements entitlements.plist $(which node)
```

The final recovery step was to remove the local Codex logs database files:

```bash
rm -rf ~/.codex/logs_2.sqlite ~/.codex/logs_2.sqlite-wal ~/.codex/logs_2.sqlite-shm
```

Verify the install:

```bash
codex --version
which codex
codex doctor
```

Start Codex in the current project:

```bash
codex
```

## Authentication

Codex supports two common authentication paths:

- ChatGPT sign-in for subscription/workspace access
- OpenAI API key for usage-based local workflows

For browser login:

```bash
codex login
```

For device-code login, useful when browser callback issues occur:

```bash
codex login --device-auth
```

For API key usage, set the environment variable before launching Codex:

```bash
export OPENAI_API_KEY="your_api_key_here"
codex
```

## Challenges and Solutions

### Challenge: Intel MacBook uses x86_64 binaries

Apple Silicon instructions sometimes assume `arm64`. On this Intel Core i7 MacBook, Codex diagnostics report `macos-x86_64`.

Solution:

Use normal npm installation and confirm Codex resolves to the x64 package:

```bash
codex doctor
```

Look for `macos-x86_64` in the diagnostic output.

### Challenge: PATH alias warning

Observed warning:

```text
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
```

Solution:

This warning did not prevent `codex --version` from running. Confirm the executable is still available:

```bash
which codex
codex --version
```

If `which codex` does not return a path, make sure npm global binaries are on the shell path. On this machine, Codex was available at:

```text
/usr/local/bin/codex
```

### Challenge: Mixed authentication signals

`codex doctor` may report mixed auth signals if both ChatGPT login and `OPENAI_API_KEY` are present.

Solution:

Choose one authentication mode for the session.

For ChatGPT login:

```bash
unset OPENAI_API_KEY
codex login
codex
```

For API key mode:

```bash
export OPENAI_API_KEY="your_api_key_here"
codex
```

### Challenge: DNS, firewall, VPN, or WebSocket issues

`codex doctor` may report WebSocket or HTTP reachability failures when the network blocks required endpoints.

Solution:

Run diagnostics:

```bash
codex doctor
```

Then check:

- VPN or corporate firewall settings
- DNS resolution
- proxy environment variables
- custom certificate authority requirements

If a network uses a custom root certificate, set:

```bash
export CODEX_CA_CERTIFICATE="/path/to/corporate-root-ca.pem"
codex login
```

### Challenge: macOS privacy prompts

macOS may ask for permission when Codex or its terminal tries to access protected folders such as Desktop, Documents, Downloads, or Music.

Solution:

Approve the prompt if Codex needs that folder, or keep projects under a development directory such as:

```text
~/Development
```

### Challenge: Codex app and Codex CLI versions may differ

The Codex desktop app and CLI can use different bundled versions.

Solution:

Check the CLI version:

```bash
codex --version
```

Check the desktop app bundled version:

```bash
/Applications/Codex.app/Contents/Resources/codex --version
```

Update the CLI with:

```bash
npm install -g @openai/codex
```

If the latest version does not work on the Intel MacBook, reinstall the known working version:

```bash
npm install -g @openai/codex@0.140.0
```

## Useful Diagnostic Commands

```bash
codex --version
which codex
codex doctor
node --version
uname -m
sw_vers
```

## Local Logs and State

Useful locations when debugging:

```text
~/.codex/auth.json
~/.codex/sessions
~/.codex/archived_sessions
~/Library/Logs/com.openai.codex
```

Treat `~/.codex/auth.json` like a password because it can contain access tokens.
