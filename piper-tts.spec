#define git 20251112
%define libname %mklibname piper
%define devname %mklibname -d piper

%bcond_without clib

Name:		piper-tts
Version:	1.5.0%{?git:~%{git}}
Release:	2
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
Requires:	python-piper-tts = %{EVRD}
# Wire voices into Speech Dispatcher when available
Recommends:	speech-dispatcher-piper

Source10:	piper-speechd-update
Source11:	piper-speechd-synth

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
piper-system-espeak-ng.patch
piper-speak-improvements.patch
piper-speak-last-chunk.patch

%description
A fast and local neural text-to-speech engine that embeds
espeak-ng for phonemization.

%package -n python-piper-tts
Summary:	Python version of the Piper text-to-speech system
Group:		System/Multimedia
Requires:	espeak-ng
# This is really a "Requires:", but since it can also be fulfilled by downloading a
# voice somewhere (and an app using piper might come with a voice), let's keep it
# a soft dependency
Recommends:	piper-voice

%description -n python-piper-tts
Python version of the Piper text-to-speech system

%package -n %{libname}
Summary:	Library for Text-to-Speech processing
Group:		System/Libraries
Requires:	espeak-ng
# This is really a "Requires:", but since it can also be fulfilled by downloading a
# voice somewhere (and an app using piper might come with a voice), let's keep it
# a soft dependency
Recommends:	piper-voice

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

%package -n speech-dispatcher-piper
Summary:	Speech Dispatcher integration for Piper voices
Group:		System/Multimedia
Requires:	piper-tts = %{EVRD}
Requires:	speech-dispatcher
Requires:	python3
# paplay is the preferred raw-PCM player used by piper-speechd-synth
Recommends:	pulseaudio-utils
# Filetriggers fire when any package drops/removes files here
Requires(post):	python3

%description -n speech-dispatcher-piper
Wires system Piper voices (/usr/share/piper/voices, from piper-voice-*
packages) into Speech Dispatcher via the generic output module.

An RPM filetrigger regenerates the Speech Dispatcher module config
whenever voices are installed or removed. Piper is set as the default
Speech Dispatcher module when at least one voice is present; create
/etc/speech-dispatcher/disable-piper-default to keep another default.

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

mkdir -p %{buildroot}%{_datadir}/piper/voices
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/modules

install -m755 %{SOURCE10} %{buildroot}%{_libexecdir}/piper-speechd-update
install -m755 %{SOURCE11} %{buildroot}%{_libexecdir}/piper-speechd-synth

%if %{with clib}
%ninja_install -C libpiper/build

cp -a piper-speak/build/piper-speak %{buildroot}%{_bindir}/

# Duplicates from espeak-ng
rm -rf %{buildroot}%{_datadir}/espeak-ng-data
%endif

%post -n speech-dispatcher-piper
%{_libexecdir}/piper-speechd-update || :

%postun -n speech-dispatcher-piper
if [ "$1" = 0 ]; then
	# Package removal: drop managed speechd block and module conf
	rm -f %{_sysconfdir}/speech-dispatcher/modules/piper.conf
	if [ -f %{_sysconfdir}/speech-dispatcher/speechd.conf ]; then
		python3 - <<'PY' || :
from pathlib import Path
import re
p = Path("%{_sysconfdir}/speech-dispatcher/speechd.conf")
t = p.read_text(encoding="utf-8", errors="replace")
t2 = re.sub(
    r"# BEGIN speech-dispatcher-piper \(auto-generated - do not edit\).*?"
    r"# END speech-dispatcher-piper \(auto-generated - do not edit\)\n?",
    "",
    t,
    flags=re.S,
)
if t2 != t:
    p.write_text(t2, encoding="utf-8")
PY
	fi
fi

# Rescan voices whenever anything under the voices directory changes.
%transfiletriggerin -n speech-dispatcher-piper -- %{_datadir}/piper/voices
%{_libexecdir}/piper-speechd-update || :
%end

%transfiletriggerpostun -n speech-dispatcher-piper -- %{_datadir}/piper/voices
%{_libexecdir}/piper-speechd-update || :
%end

%files
%{_bindir}/piper

%files -n python-piper-tts
%{python3_sitearch}/piper
%{python3_sitearch}/piper_tts-%(echo %{version} |sed -e 's,~.*,,').dist-info

%if %{with clib}
%files -n %{libname}
%{_libdir}/libpiper.so.0*
%{_libdir}/piper

%files -n %{devname}
%{_libdir}/libpiper.so
%{_includedir}/piper.h
%dir %{_datadir}/piper
%dir %{_datadir}/piper/voices

%files -n piper-speak
%{_bindir}/piper-speak
%endif

%files -n speech-dispatcher-piper
%{_libexecdir}/piper-speechd-update
%{_libexecdir}/piper-speechd-synth
%dir %{_sysconfdir}/speech-dispatcher
%dir %{_sysconfdir}/speech-dispatcher/modules
# Generated at install / by filetriggers
%ghost %{_sysconfdir}/speech-dispatcher/modules/piper.conf
