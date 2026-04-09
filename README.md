# Alien Invasion

A classic Space Invaders-style arcade game built with Python and pygame.

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Controls

| Key | Action |
|-----|--------|
| `←` / `→` | Move ship |
| `Space` | Shoot |
| `R` | Restart / next level |

## Requirements

- Python 3.8+
- pygame

```bash
pip install pygame
python3 alien_invasion.py
```

---

## Building Linux Packages

This repo includes a GitHub Actions workflow that automatically builds
`.deb` (Debian/Ubuntu) and `.rpm` (Fedora/RHEL) packages.

### Trigger a build

**Option 1 — Push a version tag** (also creates a GitHub Release):
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Option 2 — Manual trigger:**  
Go to **Actions → Build Linux Packages → Run workflow** and enter a version number.

### Download the packages

After the workflow completes, packages are available in two places:

- **Artifacts** — on any build (Actions tab → select run → Artifacts section)
- **GitHub Releases** — automatically attached when triggered by a tag push

### Installing the packages

**.deb (Debian / Ubuntu / Mint):**
```bash
sudo apt install python3-pygame
sudo dpkg -i alien-invasion_1.0.0_all.deb
alien-invasion
```

**.rpm (Fedora / RHEL / openSUSE):**
```bash
sudo dnf install python3-pygame
sudo rpm -i alien-invasion-1.0.0-1.noarch.rpm
alien-invasion
```

---

## Repository Structure

```
.
├── alien_invasion.py               ← game source
├── .github/
│   └── workflows/
│       └── build-packages.yml      ← CI/CD workflow
└── packaging/
    ├── deb/                        ← .deb package template
    │   ├── DEBIAN/
    │   │   ├── control             ← package metadata & dependencies
    │   │   └── postinst            ← post-install script
    │   └── usr/
    │       ├── games/
    │       │   └── alien-invasion  ← launcher shell script
    │       └── share/
    │           ├── applications/
    │           │   └── alien-invasion.desktop
    │           └── pixmaps/
    │               └── alien-invasion.svg
    └── rpm/
        └── alien-invasion.spec     ← RPM spec file
```

## How the workflow works

1. **Version** is extracted from the git tag (`v1.0.0` → `1.0.0`) or the manual input.
2. **build-deb** job: injects the version into `DEBIAN/control`, copies the game into the deb tree, fixes permissions, runs `fakeroot dpkg-deb --build`.
3. **build-rpm** job: installs `rpmbuild`, copies sources into `~/rpmbuild/SOURCES/`, runs `rpmbuild -bb` with the version passed as a define.
4. **release** job: only runs on tag pushes — downloads both artifacts and attaches them to a GitHub Release automatically.
