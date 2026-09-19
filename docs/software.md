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

## Bonsai dependency repair

On September 19, 2026, Bonsai's managed Python dependency directory was missing after an earlier native-library loading failure. A normal Blender startup reconstructed the environment from the extension's bundled wheels. A second fresh startup confirmed Bonsai enabled, IfcOpenShell 0.8.5 import, the IFC loading operator, and native solid tessellation (8 vertices, 12 triangles). The native IfcOpenShell library passed macOS code-signature verification; saved user preferences were unchanged.

For a similar missing-dependency failure, first close concurrent extension-management operations, start Blender normally and inspect its startup log. Use the compatible official extension's installation workflow if rebuilding its bundled environment does not resolve it. A menu entry alone is insufficient: test native geometry and reopen an actual IFC. See [official Bonsai installation guidance](https://docs.bonsaibim.org/guides/development/installation.html).

Home assembly uses `--factory-startup` to avoid unrelated add-on workspace links in saved models. Bonsai import verification uses a separate normal startup with the extension enabled. Keep the native model and the temporary imported IFC scene separate.
