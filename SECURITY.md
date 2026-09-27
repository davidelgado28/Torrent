---

### `SECURITY.md`

```markdown
# Security Policy

## Educational Use and Responsibility

This project is a conceptual and educational implementation of the BitTorrent protocol specifications. It has neither been designed nor audited for use in production environments.

- **Lack of Sandboxing:** The code processes local binary files. Do not use the client to open `.torrent` files from untrusted sources.
- **Input Validation:** Although the parser handles basic Bencode syntax errors, it lacks advanced protections against memory overflow attacks or infinite recursion caused by maliciously crafted files.

## Vulnerability Reporting

If you identify a security vulnerability in this repository's code:

1. **Do not open a public Issue.**
2. Send an email describing the vulnerability to the project maintainer at `davidelgado.tech@gmail.com`.
3. Include steps to reproduce the issue and, if possible, a suggested fix.

We appreciate your cooperation in keeping this code secure and educational.
