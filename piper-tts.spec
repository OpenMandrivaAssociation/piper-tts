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
# Keep in sync with the version requested in piper1-gpl sources
%define espeak 212928b394a96e8fd2096616bfd54e17845c48f6
Source1:	https://github.com/espeak-ng/espeak-ng/archive/%{espeak}.tar.gz
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

%prep
%autosetup -p1 -a1 -n piper1-gpl-%{?git:main}%{!?git:%{version}}
ESPEAKDIR=$(pwd)/espeak-ng-%{espeak}
# See https://github.com/espeak-ng/espeak-ng/issues/2048
sed 's/160/1024/' -i "${ESPEAKDIR}/src/libespeak-ng/speech.h"
sed -e "s|GIT_REPOSITORY.*|SOURCE_DIR ${ESPEAKDIR}|" \
	-e 's|GIT_TAG.*|DOWNLOAD_COMMAND ""|' \
	-i CMakeLists.txt libpiper/CMakeLists.txt
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
%{_bindir}/piper-speak
%{_libdir}/libpiper.so.0*
%{_libdir}/piper

%files -n %{devname}
%{_libdir}/libpiper.so
%{_includedir}/piper.h
%endif
