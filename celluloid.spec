%global debug_package %{nil}

%global glib2_version 2.40
%global gtk3_version 3.20
%global mpv_version 0.25.0
%global commit0 c47724b92742c63624c8dbe39cc2ca9d4bc8a79c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           celluloid
Version:        0.17
Release:        4.git%{shortcommit0}%{?dist}
Summary:        A simple GTK+ frontend for mpv

License:        GPLv3+
URL:            https://github.com/celluloid-player/celluloid
Source0:  	https://github.com/celluloid-player/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

# main dependencies
BuildRequires:	meson
BuildRequires:	ninja-build
BuildRequires:	mesa-libEGL-devel
BuildRequires:  gcc-c++
#BuildRequires:  autoconf-archive
#BuildRequires:  automake
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(epoxy)
BuildRequires:	pkgconfig(mpv) >= %{mpv_version}
#BuildRequires:  mpv-libs-devel mpv-libs
BuildRequires:  intltool
BuildRequires:  libappstream-glib-devel
BuildRequires:  python-devel
# for video-sharing websites playback
Requires:       hicolor-icon-theme
Requires:       youtube-dl
Requires:       lua  
Obsoletes:	gnome-mpv <= 0.16     
%description
GNOME MPV interacts with mpv via the client API exported by libmpv,
allowing access to mpv's powerful playback capabilities.

%prep
%autosetup -n %{name}-%{commit0}

%build
    meson _build --buildtype=release --prefix=/usr
    ninja-build -C _build

%install
env DESTDIR=%{buildroot} ninja -C _build install

%find_lang %{name}

%check
#appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/io.github.*.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.*.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS README.md
%license COPYING
%{_bindir}/%{name}
%{_datadir}/metainfo/io.github.*.appdata.xml
%{_datadir}/applications/io.github.*.desktop
%{_datadir}/glib-2.0/schemas/io.github.*.gschema.xml
%{_datadir}/dbus-1/services/io.github.*.service
%{_mandir}/man1/%{name}.*.gz
# The old GSchema is left installed for settings migration.
%{_datadir}/glib-2.0/schemas/org.*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*.svg


%changelog

* Mon Sep 09 2019 - David Va <davidva AT tuta DOT io> 0.17-7.gitc47724b
- Updated to 0.17-7.gitc47724b

* Wed Jan 23 2019 - David Va <davidva AT tuta DOT io> 0.16-4.git29ac47a
- Update to 0.16-4.git29ac47a

* Wed Sep 12 2018 - David Va <davidva AT tuta DOT io> 0.15-4.gitda6be82
- Update to 0.15-4.gitda6be82

* Sun Apr 08 2018 David Vásquez <davidva AT tutanota DOT com> 0.14-4.git14bee52
- Update to 0.14-4.git14bee52

* Sun Feb 18 2018 David Vásquez <davidva AT tutanota DOT com> 0.14-3.git9fe61e0
- Updated to 0.14-3.git9fe61e0

* Sun Oct 22 2017 David Vásquez <davidva AT tutanota DOT com> 0.13-3.git1ea4728
- Updated to 0.13

* Wed Sep 06 2017 David Vásquez <davidva AT tutanota DOT com> 0.12-3.git2e13ab3
- First round with meson and ninja

* Mon Jun 12 2017 David Vásquez <davidva AT tutanota DOT com> 0.12-1.git809b98e
- Updated to 0.12-1.git809b98e

* Sat Jan 07 2017 Pavlo Rudyi <paulcarroty@riseup.net> - 0.11-2
- Updated to 0.11

* Wed Nov 16 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.9-2
- Updated to 0.10

* Sun May 22 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.9-2
- Fix playlist metadata retrieval 

* Tue Apr 26 2016 Pavlo Rudyi <paulcarroty@riseup.net> - 0.8-2
- Rebuild for Fedora 24

* Mon Apr 18 2016 Maxim Orlov <murmansksity@gmail.com> - 0.8-1.R
- Update to 0.8
- Add AUTHORS %%doc
- Add mpv dep version
- Update gtk3 dep version
- Change app ID to io.github.GnomeMpv

* Sat Jan 30 2016 Maxim Orlov <murmansksity@gmail.com> - 0.7-1.R
- Update to 0.7
- Add AppData
- Add symbolic icon

* Sat Nov 14 2015 Maxim Orlov <murmansksity@gmail.com> - 0.6-3.R
- Fix E: explicit-lib-dependency mpv-libs (rpmlint)

* Fri Nov 13 2015 Maxim Orlov <murmansksity@gmail.com> - 0.6-2.R
- Update dependencies (mpv-libs-devel, mpv-libs)

* Mon Oct 26 2015 Maxim Orlov <murmansksity@gmail.com> - 0.6-1.R
- Update to 0.6
- Add autoconf-archive BR
- Add NOCONFIGURE=1 ./autogen.sh
- Add V=1 (Make the build verbose)
- Remove autoreconf, intltoolize calls

* Sat Oct 17 2015 Maxim Orlov <murmansksity@gmail.com> - 0.5-2.R
- Remove requires mpv
- Minor spec cleanup

* Mon Aug 17 2015 Maxim Orlov <murmansksity@gmail.com> - 0.5-1.R
- Initial package.
