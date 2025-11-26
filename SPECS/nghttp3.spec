# Supported targets: el8, el9, el10

%define _prefix /opt/%{name}
%define _docdir_fmt nghttp3

%{!?make_verbose: %define make_verbose 0}

%if 0%{?rhel} <= 8
%undefine __cmake_in_source_build
%endif

%global source_date_epoch_from_changelog 0

Name: nghttp3-0z
Version: 1.13.1
Release: 1%{?dist}.zenetys
Summary: nghttp3 HTTP/3 library written in C
License: MIT
URL: https://github.com/ngtcp2/nghttp3

Source0: https://github.com/ngtcp2/nghttp3/releases/download/v%{version}/nghttp3-%{version}.tar.gz

BuildRequires: cmake >= 3.20
BuildRequires: gcc

%description
nghttp3 is an implementation of RFC 9114 HTTP/3 mapping over QUIC
and RFC 9204 QPACK in C. It does not depend on any particular QUIC
transport implementation.

%prep
%setup -n nghttp3-%{version}

%build
# Fake CXX compiler to /bin/true because it is not needed when
# building with ENABLE_LIB_ONLY.
%cmake \
    %if !%{make_verbose}
    -DCMAKE_VERBOSE_MAKEFILE=OFF \
    %endif
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DENABLE_LIB_ONLY=ON \
    -DENABLE_STATIC_LIB=OFF \
    -DCMAKE_CXX_COMPILER=/bin/true

# use --define 'make_verbose 1' to enable verbose
%(x='%{cmake_build}'; echo ${x/ --verbose})

%install
%cmake_install
rm -rf %{buildroot}%{_prefix}/lib/cmake

mkdir -p %{buildroot}%{_rpmmacrodir}
echo '%%%(echo %{name} |tr '-' '_')_prefix %{_prefix}' \
    > %{buildroot}%{_rpmmacrodir}/macros.%{name}

%files
%doc README.rst
%license COPYING

%{_libdir}/libnghttp3.so.*

%package devel
Summary: nghttp3 development files from package %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
nghttp3 development files from package %{name}.

%files devel
%{_includedir}/nghttp3
%{_libdir}/libnghttp3.so
%{_libdir}/pkgconfig/libnghttp3.pc
%{_rpmmacrodir}/macros.%{name}
