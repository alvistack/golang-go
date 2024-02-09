# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global __strip /bin/true

%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post \
    /usr/lib/rpm/check-rpaths \
    /usr/lib/rpm/check-buildroot \
    /usr/lib/rpm/brp-compress

%undefine _build_create_debug
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true NO_BRP_AR=true

Name: golang-1.23
Epoch: 100
Version: 1.23.1
Release: 1%{?dist}
Summary: Go programming language
License: BSD-3-Clause
URL: https://github.com/golang/go/tags
Source0: %{name}_%{version}.orig.tar.gz
Source99: %{name}.rpmlintrc
BuildRequires: fdupes
BuildRequires: golang-1.20
BuildRequires: net-tools

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

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
set -ex && \
    export GOROOT=%{buildroot} && \
    export GOROOT_FINAL=%{_libdir}/go-1.23 && \
    cd ./src && \
    bash ./make.bash

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_libdir}/go-1.23
install -Dpm755 -d %{buildroot}%{_docdir}/go-1.23/html
cp -rfp VERSION %{buildroot}%{_libdir}/go-1.23/
cp -rfp api %{buildroot}%{_libdir}/go-1.23/
cp -rfp bin %{buildroot}%{_libdir}/go-1.23/
cp -rfp doc/* %{buildroot}%{_docdir}/go-1.23/html/
cp -rfp go.env %{buildroot}%{_libdir}/go-1.23/
cp -rfp misc %{buildroot}%{_libdir}/go-1.23/
cp -rfp pkg %{buildroot}%{_libdir}/go-1.23/
cp -rfp src %{buildroot}%{_libdir}/go-1.23/
cp -rfp test %{buildroot}%{_libdir}/go-1.23/
find %{buildroot}%{_libdir}/go-1.23/src -type f -name '*.rc' -delete
ln -fs %{_libdir}/go-1.23/bin/go %{buildroot}%{_bindir}/go
ln -fs %{_libdir}/go-1.23/bin/gofmt %{buildroot}%{_bindir}/gofmt
fdupes -qnrps %{buildroot}%{_prefix}

%check

%package -n go
BuildArch: noarch
Summary: Go programming language
Requires: golang-1.23 = %{epoch}:%{version}-%{release}

%description -n go
Go programming language.

%package -n golang
BuildArch: noarch
Summary: Go programming language
Requires: golang-1.23 = %{epoch}:%{version}-%{release}

%description -n golang
Go programming language.

%package -n golang-src
BuildArch: noarch
Summary: Go programming language
Requires: golang-1.23 = %{epoch}:%{version}-%{release}

%description -n golang-src
Go programming language.

%package -n golang-bin
BuildArch: noarch
Summary: Go programming language
Requires: golang-1.23 = %{epoch}:%{version}-%{release}

%description -n golang-bin
Go programming language.

%files
%license LICENSE
%dir %{_libdir}/*
%dir %{_docdir}/*
%{_bindir}/*
%{_libdir}/*
%{_docdir}/*

%files -n go
%license LICENSE

%files -n golang
%license LICENSE

%files -n golang-src
%license LICENSE

%files -n golang-bin
%license LICENSE

%changelog
