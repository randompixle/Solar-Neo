# Solar neo — Universal APT-Style Package Installer for Every Linux Distro

**Sola Neo** lets you use APT-style commands on distros that **don’t use apt**  
(Bazzite / Fedora rpm-ostree, Arch, etc.) — *no extra setup needed.*

Auto-detects your system backend  
Automatically uses sudo when needed  
Flatpak fallback when system package missing  
Supports AUR if installed (yay/paru)  
Unified installed app listing (system + flatpak)

> Just type `neo install <package>`

---

##  Features/Documentation

- Cross-distro support:
  - **rpm-ostree** (Bazzite, Silverblue)
  - **DNF / DNF5** (Fedora)
  - **Pacman** (Arch-based)
  - **APT** (Debian/Ubuntu)
  - **Flatpak** (fallback)
  - **AUR** helper if available
- Commands:
  ```bash
  solar install <pkg>
  solar remove <pkg>
  soalr search <pkg>
  solar info <pkg>
  solar list
  solar update
  solar upgrade
  solar backend list
  solar setup
  solar self-update
