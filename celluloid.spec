%global debug_package %{nil}

%global glib2_version 2.40
%global gtk4_version 3.0
%global mpv_version 0.25.0
%global commit0 6cc8ad5444541c2a0bf028efeb01b1f1d7bcec4a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Force out of source build
%undefine __cmake_in_source_build


Name:           celluloid
Version:        0.22
Release:        7.git%{shortcommit0}%{?dist}
Summary:        A simple GTK+ frontend for mpv

License:        GPLv3+
URL:            https://github.com/celluloid-player/celluloid
Source0:  	https://github.com/celluloid-player/celluloid/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

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
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(epoxy)
BuildRequires:	pkgconfig(mpv) >= %{mpv_version}
#Wtf?
BuildRequires:	opus libogg libsndfile flac-libs
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
meson _build --buildtype=release --prefix=/usr --libdir=%{_libdir} --libexecdir=/usr/libexec --bindir=/usr/bin --sbindir=/usr/sbin --includedir=/usr/include --datadir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --localedir=/usr/share/locale --sysconfdir=/etc

%meson_build -C _build

%install
%meson_install -C _build 

%find_lang %{name}

%check
#appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/io.github.*.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.celluloid_player.Celluloid.desktop

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
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_mandir}/man1/celluloid*.gz
%{_datadir}/metainfo/*.appdata.xml


%changelog

* Fri Nov 12 2021 - David Va <davidva AT tuta DOT io> 0.22-7.git6cc8ad5
- Updated to 0.22

* Thu Apr 15 2021 - David Va <davidva AT tuta DOT io> 0.21-7.gitc77fbeb
- Updated to 0.21

* Mon Sep 21 2020 - David Va <davidva AT tuta DOT io> 0.20-7.git9cfab01
- Updated to 0.20

* Thu Apr 09 2020 - David Va <davidva AT tuta DOT io> 0.19-7.git7784d91
- Updated to 0.19

* Wed Nov 06 2019 - David Va <davidva AT tuta DOT io> 0.18-7.gite23a68d
- Updated to 0.18

* Thu Oct 31 2019 - David Va <davidva AT tuta DOT io> 0.17-10.git5df3893
- Updated to current commit

* Mon Sep 23 2019 - David Va <davidva AT tuta DOT io> 0.17-9.git6fca3f1
- Updated to current commit
- Fixes around mpv crash when running keyup command without argum

* Sat Sep 14 2019 - David Va <davidva AT tuta DOT io> 0.17-8.gitc47724b
- Updated to current commit

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
