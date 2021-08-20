%global debug_package %{nil}

%global __strip /bin/true

%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post \
    /usr/lib/rpm/check-rpaths \
    /usr/lib/rpm/check-buildroot \
    /usr/lib/rpm/brp-compress

%undefine _build_create_debug
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true NO_BRP_AR=true

Name: golang-1.17
Epoch: 100
Version: 1.17
Release: 1%{?dist}
Summary: Go programming language
License: BSD-3-Clause
URL: https://github.com/golang/go/releases
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
BuildRequires: go
%else
BuildRequires: golang-bin
BuildRequires: golang-src
%endif
BuildRequires: fdupes
BuildRequires: net-tools
Requires(post): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
Provides: golang-1.17-devel = %{epoch}:%{version}-%{release}
Provides: golang-1.17 = %{epoch}:%{version}-%{release}
Provides: golang-1.17-go = %{epoch}:%{version}-%{release}
Provides: golang-1.17-src = %{epoch}:%{version}-%{release}
Provides: golang-1.17-doc = %{epoch}:%{version}-%{release}

%description
The Go programming language is an open source project to make
programmers more productive. Go is expressive, concise, clean, and
efficient. Its concurrency mechanisms make it easy to write programs
that get the most out of multicore and networked machines, while its
novel type system enables flexible and modular program construction. Go
compiles quickly to machine code yet has the convenience of garbage
collection and the power of run-time reflection. It's a fast, statically
typed, compiled language that feels like a dynamically typed,
interpreted language.

%package -n golang
Summary: Go programming language - metapackage
Requires: golang-1.17
Provides: go = %{epoch}:%{version}-%{release}
Provides: golang = %{epoch}:%{version}-%{release}

%description -n golang
This is a dependency package that depends on the default Go toolchain
and compiled standard library.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
set -ex && \
    cd ./src && \
    export GOROOT=%{buildroot} && \
    export GOROOT_FINAL=%{_libdir}/go-1.17 && \
    bash ./make.bash

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_libdir}/go-1.17
install -Dpm755 -d %{buildroot}%{_docdir}/go-1.17/html
cp -rfp VERSION %{buildroot}%{_libdir}/go-1.17/
cp -rfp api %{buildroot}%{_libdir}/go-1.17/
cp -rfp bin %{buildroot}%{_libdir}/go-1.17/
cp -rfp doc/* %{buildroot}%{_docdir}/go-1.17/html/
cp -rfp misc %{buildroot}%{_libdir}/go-1.17/
cp -rfp pkg %{buildroot}%{_libdir}/go-1.17/
cp -rfp src %{buildroot}%{_libdir}/go-1.17/
cp -rfp test %{buildroot}%{_libdir}/go-1.17/
find %{buildroot}%{_libdir}/go-1.17/src -type f -name '*.rc' -delete
ln -fs %{_libdir}/go-1.17/bin/go %{buildroot}%{_bindir}/go1.17
ln -fs %{_libdir}/go-1.17/bin/gofmt %{buildroot}%{_bindir}/gofmt1.17
ln -fs %{_sysconfdir}/alternatives/go %{buildroot}%{_bindir}/go
ln -fs %{_sysconfdir}/alternatives/gofmt %{buildroot}%{_bindir}/gofmt
%fdupes -s %{buildroot}%{_prefix}

%post
%{_sbindir}/update-alternatives \
    --install %{_bindir}/go go %{_libdir}/go-1.17/bin/go 170 \
    --slave %{_bindir}/gofmt gofmt %{_libdir}/go-1.17/bin/gofmt

%preun
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --remove go %{_libdir}/go-1.17/bin/go
fi

%files
%license LICENSE
%ghost %{_sysconfdir}/alternatives/go
%ghost %{_sysconfdir}/alternatives/gofmt
%dir %{_libdir}/go-1.17
%dir %{_docdir}/go-1.17
%dir %{_docdir}/go-1.17/html
%{_bindir}/go
%{_bindir}/go1.17
%{_bindir}/gofmt
%{_bindir}/gofmt1.17
%{_libdir}/go-1.17
%{_docdir}/go-1.17

%changelog
%files -n golang
%license LICENSE

