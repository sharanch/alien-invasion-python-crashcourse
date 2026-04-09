Name:       alien-invasion
Version:    %{version_tag}
Release:    1
Summary:    Classic Alien Invasion arcade game
License:    MIT
BuildArch:  noarch
Requires:   python3 >= 3.8

%description
A pygame-based Space Invaders-style game with animated aliens,
multi-level progression, particle explosions, and a scrolling starfield.
Use arrow keys to move and Space to shoot.
Requires python3-pygame to be installed.

%install
mkdir -p %{buildroot}/usr/games
mkdir -p %{buildroot}/usr/share/games/alien-invasion
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/pixmaps

install -m 755 %{_sourcedir}/alien-invasion.sh \
    %{buildroot}/usr/games/alien-invasion
install -m 644 %{_sourcedir}/alien_invasion.py \
    %{buildroot}/usr/share/games/alien-invasion/alien_invasion.py
install -m 644 %{_sourcedir}/alien-invasion.desktop \
    %{buildroot}/usr/share/applications/alien-invasion.desktop
install -m 644 %{_sourcedir}/alien-invasion.svg \
    %{buildroot}/usr/share/pixmaps/alien-invasion.svg

%files
%attr(0755, root, root) /usr/games/alien-invasion
%attr(0644, root, root) /usr/share/games/alien-invasion/alien_invasion.py
%attr(0644, root, root) /usr/share/applications/alien-invasion.desktop
%attr(0644, root, root) /usr/share/pixmaps/alien-invasion.svg

%changelog
* Mon Jan 01 2024 Your Name <you@example.com> - 1.0.0-1
- Initial release
