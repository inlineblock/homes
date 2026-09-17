# Working together

1. Install the software versions listed in the home's `project.json`, plus Git LFS.
2. Clone the full repository and run `git lfs pull` before opening models.
3. Create a branch for your changes. Coordinate ownership of each `.blend` or `.ifc`: these files do not merge like source code.
4. Use relative asset links and commit new dependencies with the home. For a changed shared asset, publish a new version folder.
5. Commit source, curated previews, approved exports, and the updated project manifest. Temporary renders, caches, and automatic Blender backups are ignored.
6. Push your branch and review a preview or drawing alongside the changes. Git LFS uploads the large files to the hosting provider separately from normal Git objects.

Check a fresh clone before handing a project off. A downloaded ZIP may not include LFS content depending on host settings; cloning with LFS is the supported workflow. Hosting providers may charge for LFS storage and bandwidth.

To verify portability from a clone, run `blender --background --python-exit-code 1 --python tools/common/verify_repository.py`. It reopens each native home, checks that library paths stay inside the clone, and measures the enclosed slabs. This verifies local file portability; it does not verify a remote hosting account or its LFS quota.

When publishing, choose a repository host and visibility deliberately. No remote is created automatically by this starter. Do not commit precise client addresses, surveys, or client reference photos without deciding who should receive them.

Reference: https://docs.github.com/en/repositories/working-with-files/managing-large-files/collaboration-with-git-large-file-storage
