%define gitver %(echo %version | tr _ -)
Name:          piper-tts
Version:       2023.11.14_2
Release:       1
Summary:       A fast, local neural text to speech system
Group:         Applications/Multimedia
URL:           https://rhasspy.github.io/piper-samples/
Source0:       https://github.com/rhasspy/piper/archive/%{gitver}/%{name}-%{gitver}.tar.gz
Source1:       https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx
Source2:       https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json
Source3:       https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/karlsson/low/de_DE-karlsson-low.onnx
Source4:       https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/karlsson/low/de_DE-karlsson-low.onnx.json
Source5:       https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/gosia/medium/pl_PL-gosia-medium.onnx
Source6:       https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/gosia/medium/pl_PL-gosia-medium.onnx.json
Source7:       https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx
Source8:       https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx.json
Source9:       https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx
Source10:      https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json
Source11:      https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx
Source12:      https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json
Source13:      https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/low/en_GB-alan-low.onnx
Source14:      https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/low/en_GB-alan-low.onnx.json
#Patch0:        piper-tts-2023.11.14_2-system-dependencies.patch
License:       MIT

BuildRequires: glibc-devel
# Need import
#BuildRequires: libespeak-ng-devel
BuildRequires: pkgconfig(fmt)
# Need import
BuildRequires: libpiper-phonemize-devel
BuildRequires: pkgconfig(spdlog)
BuildRequires: cmake

%description
A fast, local neural text to speech system.

%prep
%autosetup -n piper-%{gitver} -p1

%build
%cmake \
   -DPIPER_PHONEMIZE_DIR=%{_prefix}

%make_build

%install
%make_install -C build

install -d -m0755 %{buildroot}%{_bindir}
mv %{buildroot}{%{_prefix},%{_bindir}}/piper

install -D -m0644 %{SOURCE1} %{buildroot}%{_datadir}/piper-voices/de_DE-thorsten-medium.onnx
install -D -m0644 %{SOURCE2} %{buildroot}%{_datadir}/piper-voices/de_DE-thorsten-medium.onnx.json
install -D -m0644 %{SOURCE3} %{buildroot}%{_datadir}/piper-voices/de_DE-karlsson-low.onnx
install -D -m0644 %{SOURCE4} %{buildroot}%{_datadir}/piper-voices/de_DE-karlsson-low.onnx.json
install -D -m0644 %{SOURCE5} %{buildroot}%{_datadir}/piper-voices/pl_PL-gosia-medium.onnx
install -D -m0644 %{SOURCE6} %{buildroot}%{_datadir}/piper-voices/pl_PL-gosia-medium.onnx.json
install -D -m0644 %{SOURCE7} %{buildroot}%{_datadir}/piper-voices/pl_PL-darkman-medium.onnx
install -D -m0644 %{SOURCE8} %{buildroot}%{_datadir}/piper-voices/pl_PL-darkman-medium.onnx.json
install -D -m0644 %{SOURCE9} %{buildroot}%{_datadir}/piper-voices/en_GB-alba-medium.onnx
install -D -m0644 %{SOURCE10} %{buildroot}%{_datadir}/piper-voices/en_GB-alba-medium.onnx.json
install -D -m0644 %{SOURCE11} %{buildroot}%{_datadir}/piper-voices/en_GB-alan-medium.onnx
install -D -m0644 %{SOURCE12} %{buildroot}%{_datadir}/piper-voices/en_GB-alan-medium.onnx.json
install -D -m0644 %{SOURCE13} %{buildroot}%{_datadir}/piper-voices/en_GB-alan-low.onnx
install -D -m0644 %{SOURCE14} %{buildroot}%{_datadir}/piper-voices/en_GB-alan-low.onnx.json


%files
%{_bindir}/piper
%doc LICENSE.md

%package voices-en
Group:         System/Multimedia
Summary:       English voices for %{name}
Requires:      piper-tts = %{EVRD}

%description voices-en
This package contains the english language voices for %{name}.

%files voices-en
%{_datadir}/piper-voices/en_GB-*.onnx
%{_datadir}/piper-voices/en_GB-*.onnx.json

%package voices-pl
Group:         System/Multimedia
Summary:       Polish voices for %{name}
Requires:      piper-tts = %{EVRD}

%description voices-pl
This package contains the polish language voices for %{name}.

%files voices-pl
%{_datadir}/piper-voices/pl_PL-*.onnx
%{_datadir}/piper-voices/pl_PL-*.onnx.json

# :D xD
%package voices-de-smuggler-pay-reparations
Group:         System/Multimedia
Summary:       German voices for %{name}
Requires:      piper-tts = %{EVRD}

%description voices-de-smuggler-pay-reparations
This package contains the german language voices for %{name}.

%files voices-de-smuggler-pay-reparations
%{_datadir}/piper-voices/de_DE-*.onnx
%{_datadir}/piper-voices/de_DE-*.onnx.json
