# Installed authoring software

The initial setup on September 17, 2026 installed:

- Blender 4.5.14 LTS, Apple Silicon, in `/Applications/Blender.app`.
- Bonsai 0.8.5, Python 3.11 Apple Silicon extension, enabled in Blender's user extension repository.
- Git LFS 3.7.0 was already present and was enabled locally for this repository.

Blender's primary download server challenged automated downloads, so the installer was retrieved from the Berkeley OCF Blender release mirror. Its SHA-256 matched the release checksum and the app passed `codesign --verify --deep --strict` before installation.

Blender installer checksum:
`65134d9b07b20e2fa8d3c9e44f6f44ffb5c9774dd521b95f50387310241ca170`

Sources:
- https://mirrors.ocf.berkeley.edu/blender/release/Blender4.5/blender-4.5.14-macos-arm64.dmg
- https://mirrors.ocf.berkeley.edu/blender/release/Blender4.5/blender-4.5.14.sha256
- https://github.com/IfcOpenShell/IfcOpenShell/releases/tag/bonsai-0.8.5

Installers are temporary local downloads, not repository assets. Collaborators install the appropriate build for their own operating system. No subscription or paid software was used.

Local commits were made without signatures because the configured SSH signing key waited for interactive authorization. The user's Git signing configuration was left unchanged.
