#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kalzium
Summary:	Kalzium
Name:		ka6-%{kaname}
Version:	25.12.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	af583220e256e755798753fedafc7a96
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6OpenGL-devel
BuildRequires:	Qt6Scxml-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kplotting-devel >= %{kframever}
BuildRequires:	kf6-kunitconversion-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	ocaml-facile
BuildRequires:	openbabel-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kalzium is your digital replacement for the periodic table on paper.
It is a program that visualizes the Periodic Table of Elements (PSE)
and includes basic information about all common elements in the PSE.
It has a gained much more functions over time.

Features

- versatile overview of all important data from the elements like
  melting points, electron affinity, electronegativity, electron
  configuration, radii, mass, ionisation energy
- tool to visualize the spectral lines of each element
- different colored views of the PSE: separation of the different
  blocks, Year simulator, Temperature simulator
- Molecular weight calculator
- an Isotope table
- 3D molecule editor, with a load and save functionality
- an equation solver for stoichiometric problems
- filetype conversion for different types of chemical programs
- tool to produce a comprehensive list of all
  Risk_and_Safety_Statements

%description -l pl.UTF-8
Kalzium jest Twoim cyfrowym zastępnikiem dla okresowej tablicy
pierwiastków na papierze. Wyświetla Okresowy Układ Pierwiastków (OUP)
podając podstawowe informacje o pierwiastkach. Z czasem otrzymuje
coraz więcej funkcji.

Właściwości

- wszechstronny opis wszystkich ważnych informacji o pierwiastkach,
  jak temperatura topnienia, powinowactwo elektronowe, elektroujemność,
  konfiguracja elektronowa, promieniotwórczość, masa atomowa, promień
  atomowy, energia jonizacyjna
- narzędzie do wizualizacji linii widmowych
- kolorowe rozróżnienia OUP: oddzielne dla różnych grup, symulator
  roku, symulator temperatury
- kalkulator masy cząsteczek
- tabela izotopów
- edytor cząsteczek 3D, z opcją wczytywania i zapisywania
- rozwiązywanie równań chemicznych
- konwerter plików do różnych formatów używanych przez programy
  chemiczne
- narzędzie do pokazywania wszechstronnej listy komunikatów zagrożeń i
  bezpieczeństwa

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kalzium
%ghost %{_libdir}/libscience.so.5
%{_libdir}/libscience.so.*.*

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.kalzium.desktop
%{_desktopdir}/org.kde.kalzium_cml.desktop
%{_datadir}/config.kcfg/kalzium.kcfg
%{_iconsdir}/hicolor/*x*/apps/kalzium.png
%{_iconsdir}/hicolor/scalable/apps/kalzium.svgz
%{_datadir}/kalzium
%dir %{_datadir}/libkdeedu
%dir %{_datadir}/libkdeedu/data
%{_datadir}/libkdeedu/data/elements.xml
%{_datadir}/libkdeedu/data/isotopes.xml
%{_datadir}/libkdeedu/data/spectra.xml
%{_datadir}/libkdeedu/data/symbols.csv
%{_datadir}/libkdeedu/data/symbols2.csv
%{_mandir}/man1/kalzium.1*
%{_datadir}/metainfo/org.kde.kalzium.appdata.xml
%{_datadir}/qlogging-categories6/kalzium.categories
%{_mandir}/ca/man1/kalzium.1*
%{_mandir}/da/man1/kalzium.1*
%{_mandir}/de/man1/kalzium.1*
%{_mandir}/es/man1/kalzium.1*
%{_mandir}/et/man1/kalzium.1*
%{_mandir}/fr/man1/kalzium.1*
%{_mandir}/gl/man1/kalzium.1*
%{_mandir}/it/man1/kalzium.1*
%{_mandir}/nl/man1/kalzium.1*
%{_mandir}/pl/man1/kalzium.1*
%{_mandir}/pt/man1/kalzium.1*
%{_mandir}/pt_BR/man1/kalzium.1*
%{_mandir}/ru/man1/kalzium.1*
%{_mandir}/sv/man1/kalzium.1*
%{_mandir}/uk/man1/kalzium.1*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/libkdeedu
%{_includedir}/libkdeedu/chemicaldataobject.h
%{_includedir}/libkdeedu/element.h
%{_includedir}/libkdeedu/elementparser.h
%{_includedir}/libkdeedu/isotope.h
%{_includedir}/libkdeedu/isotopeparser.h
%{_includedir}/libkdeedu/moleculeparser.h
%{_includedir}/libkdeedu/parser.h
%{_includedir}/libkdeedu/psetables.h
%{_includedir}/libkdeedu/science_export.h
%{_includedir}/libkdeedu/spectrum.h
%{_includedir}/libkdeedu/spectrumparser.h
%{_libdir}/libscience.so
