%define gitver %(echo %version | tr _ -)
Name:          piper-tts
Version:       2023.11.14_2
Release:       2mamba
Summary:       A fast, local neural text to speech system
Group:         Applications/Multimedia
Vendor:        openmamba
Distribution:  openmamba
Packager:      Silvan Calarco <silvan.calarco@mambasoft.it>
URL:           https://rhasspy.github.io/piper-samples/
Source:        https://github.com/rhasspy/piper.git/%{gitver}/piper-%{version}.tar.bz2
Source1:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx
Source2:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json
Source3:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx
Source4:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json
Source5:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/low/en_GB-alan-low.onnx
Source6:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/low/en_GB-alan-low.onnx.json
Source7:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx
Source8:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json
Source9:       https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx
Source10:      https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json
Patch0:        piper-tts-2023.11.14_2-system-dependencies.patch
License:       MIT
## AUTOBUILDREQ-BEGIN
BuildRequires: glibc-devel
BuildRequires: libespeak-ng-devel
BuildRequires: libfmt-devel
BuildRequires: libpiper-phonemize-devel
BuildRequires: libspdlog-devel
## AUTOBUILDREQ-END
BuildRequires: libspdlog-devel >= 0:1.15.0-1mamba
BuildRequires: cmake

%description
A fast, local neural text to speech system.

%package voices-en
Group:         System/Multimedia
Summary:       English voices for %{name}
Requires:      piper-tts = %{?epoch:%epoch:}%{version}-%{release}

%description voices-en
This package contains the english language voices for %{name}.

%debug_package

%prep
%setup -q -n piper-%{version}
%patch 0 -p1

%build
%cmake \
   -DPIPER_PHONEMIZE_DIR=%{_prefix}

%cmake_build

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
%cmake_install

install -d -m0755 %{buildroot}%{_bindir}
mv %{buildroot}{%{_prefix},%{_bindir}}/piper

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%{_bindir}/piper
%doc LICENSE.md

%files voices-en
%defattr(-,root,root)
%{_datadir}/piper-voices/en_GB-*.onnx
%{_datadir}/piper-voices/en_GB-*.onnx.json
