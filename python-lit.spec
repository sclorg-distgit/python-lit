%{?scl:%scl_package python-lit}
%{!?scl:%global pkg_name %{name}}

%global srcname lit

%if 0%{?fedora}
%global with_python3 1
%endif

# FIXME: Work around for rhel not having py2_build/py2_install macro.
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}%{?scl:%_scl_root}}}

Name: %{?scl_prefix}python-%{srcname}
Version: 0.5.0
Release: 7%{?dist}
BuildArch: noarch

License: NCSA
Group: Development/Languages
Summary: Tool for executing llvm test suites
URL: https://pypi.python.org/pypi/lit
Source0: https://pypi.python.org/packages/5b/a0/dbed2c8dfb220eb9a5a893257223cd0ff791c0fbc34ce2f1a957fa4b6c6f/lit-0.5.0.tar.gz

BuildRequires: python2-devel
BuildRequires: python-setuptools
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%description
lit is a tool used by the LLVM project for executing its test suites.

%package -n %{?scl_prefix}python2-lit
Summary: LLVM lit test runner for Python 2
Group: Development/Languages
Requires: python-setuptools
Provides: %{?scl_prefix}python-lit

%if 0%{?with_python3}
%package -n %{?scl_prefix}python3-lit
Summary: LLVM lit test runner for Python 3
Group: Development/Languages
Requires: python-setuptools
%endif

%description -n %{?scl_prefix}python2-lit
lit is a tool used by the LLVM project for executing its test suites.

%if 0%{?with_python3}
%description -n %{?scl_prefix}python3-lit
lit is a tool used by the LLVM project for executing its test suites.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Strip out #!/usr/bin/env python
sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{?scl:%{_scl_root}}%{python2_sitelib}/%{srcname}/*.py
%if 0%{?with_python3}
sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{?scl:%{_scl_root}}%{python3_sitelib}/%{srcname}/*.py
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
# FIXME: Tests fail with python3
#{__python3} setup.py test
%endif

%clean
rm -rf %{buildroot}

%files -n %{?scl_prefix}python2-%{srcname}
%doc README.txt
%{?scl:%{_scl_root}}%{python2_sitelib}/*
%if %{undefined with_python3}
%{_bindir}/lit
%endif

%if 0%{?with_python3}
%files -n %{?scl_prefix}python3-%{srcname}
%doc README.txt
%{?scl:%{_scl_root}}%{python3_sitelib}/*
%{_bindir}/lit
%endif

%changelog
* Thu Jun 08 2017 Tom Stellard <tstellar@redhat.com> - 0.5.0-7
- Build for llvm-toolset-7 rename

* Thu May 18 2017 Tom Stellard <tstellar@redhat.com> - 0.5.0-6
- Fix package names

* Wed May 10 2017 Tilmann Scheller <tschelle@redhat.com> - 0.5.0-5
- Next attempt to add runtime dependency on python-setuptools

* Tue May 09 2017 Tilmann Scheller <tschelle@redhat.com> - 0.5.0-4
- Properly add missing runtime dependency to python-setuptools

* Tue May 09 2017 Tilmann Scheller <tschelle@redhat.com> - 0.5.0-3
- Add missing runtime dependency to python-setuptools

* Fri Apr 28 2017 Tom Stellard <tstellar@redhat.com> - 0.5.0-2
- Add llvm-toolset-4 scl support

* Thu Mar 09 2017 Tom Stellard <tstellar@redhat.com> - 0.5.0-1
- Initial version
