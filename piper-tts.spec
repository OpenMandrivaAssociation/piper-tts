%define git 20250910
%define libname %mklibname piper
%define devname %mklibname -d piper

%bcond_without clib

Name:		piper-tts
Version:	1.3.1%{?git:~%{git}}
Release:	1
%if 0%{?git:1}
Source0:	https://github.com/OHF-Voice/piper1-gpl/archive/refs/heads/main.tar.gz#/%{name}-%{git}.tar.gz
%else
Source0:	https://github.com/OHF-Voice/piper1-gpl/archive/refs/tags/v%{version}.tar.gz
%endif
Summary:	Text-to-Speech system
# Also https://github.com/rhasspy/piper
URL:		https://github.com/OHF-Voice/piper1-gpl
License:	GPL-3.0
Group:		System/Multimedia
BuildSystem:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(scikit-build)
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(nlohmann_json)
BuildRequires:	pkgconfig(libonnxruntime)
BuildRequires:	pkgconfig(espeak-ng)
# Only for piper-speak
BuildRequires:	pcaudiolib-devel
# For data files that could also get installed as duplicates here
Requires:	espeak-ng
# This is really a "Requires:", but since it can also be fulfilled by downloading a
# voice somewhere (and an app using piper might come with a voice), let's keep it
# a soft dependency
Recommends:	piper-voice

%patchlist
https://github.com/OHF-Voice/piper1-gpl/pull/17.patch
https://github.com/OHF-Voice/piper1-gpl/pull/80.patch
libpiper-system-onnxruntime.patch
piper-system-json.patch
libpiper-soname.patch
libpiper-install-location.patch
libpiper-onnxruntime-1.20.1.patch
piper-speak-compile.patch
piper-speak-system-voices.patch
piper-system-voices.patch
# There's no such thing as -ac
piper-fix-ffplay-arguments.patch
piper-system-espeak-ng.patch
piper-speak-improvements.patch

%description
A fast and local neural text-to-speech engine that embeds
espeak-ng for phonemization.

%package -n %{libname}
Summary:	Library for Text-to-Speech processing
Group:		System/Libraries
# For data files that could also get installed as duplicates here
Requires:	espeak-ng

%description -n %{libname}
Library for Text-to-Speech processing

%package -n %{devname}
Summary:	Development files for the piper Text-to-Speech library
Group:		Development/C and C++
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the piper Text-to-Speech library

%package -n piper-speak
Summary:	Application for Text-to-Speech conversion using libpiper
Requires:	%{libname} = %{EVRD}
Group:		Video/Multimedia

%description -n piper-speak
Application for Text-to-Speech conversion using libpiper

%prep
%autosetup -p1 -n piper1-gpl-%{?git:main}%{!?git:%{version}}
# We use the system version
rm -f libpiper/include/json.hpp

%if %{with clib}
%build -a
# libpiper needs to be built separately
cd libpiper
%cmake -G Ninja
%ninja_build

cd ../../piper-speak
%cmake -G Ninja
%ninja_build
%endif

%install -a
rm -f %{buildroot}%{_prefix}/COPYING

%if %{with clib}
%ninja_install -C libpiper/build

cp -a piper-speak/build/piper-speak %{buildroot}%{_bindir}/

# Duplicates from espeak-ng
rm -rf %{buildroot}%{_datadir}/espeak-ng-data
%endif

%files
%{_bindir}/piper
%{python3_sitearch}/piper
%{python3_sitearch}/piper_tts-%(echo %{version} |sed -e 's,~.*,,').dist-info

%if %{with clib}
%files -n %{libname}
%{_libdir}/libpiper.so.0*
%{_libdir}/piper

%files -n %{devname}
%{_libdir}/libpiper.so
%{_includedir}/piper.h

%files -n piper-speak
%{_bindir}/piper-speak
%endif
