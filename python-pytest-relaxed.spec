#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (TODO: requires releases module)
%bcond_with	tests	# unit tests (some failures)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Relaxed test discovery/organization for pytest
Summary(pl.UTF-8):	Rozluźnione wyszukiwanie/organizacja testów dla pytesta
Name:		python-pytest-relaxed
# keep 1.x here for python2 support
Version:	1.1.5
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-relaxed/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-relaxed/pytest-relaxed-%{version}.tar.gz
# Source0-md5:	86bd9f3ecafe6fcb09c7ec67e2556672
Patch0:		%{name}-requires.patch
URL:		https://pypi.org/project/pytest-relaxed/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-decorator >= 4
BuildRequires:	python-pytest >= 3
BuildRequires:	python-six >= 1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-decorator >= 4
BuildRequires:	python3-pytest >= 3
BuildRequires:	python3-six >= 1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-releases
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pytest-relaxed provides "relaxed" test discovery for pytest.

%description -l pl.UTF-8
pytest-relaxed pozwala na "złagodzone" wyszukiwanie testów dla
pytesta.

%package -n python3-pytest-relaxed
Summary:	Relaxed test discovery/organization for pytest
Summary(pl.UTF-8):	Rozluźnione wyszukiwanie/organizacja testów dla pytesta
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pytest-relaxed
pytest-relaxed provides "relaxed" test discovery for pytest.

%description -n python3-pytest-relaxed -l pl.UTF-8
pytest-relaxed pozwala na "złagodzone" wyszukiwanie testów dla
pytesta.

%package apidocs
Summary:	API documentation for Python pytest-relaxed module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-relaxed
Group:		Documentation

%description apidocs
API documentation for Python pytest-relaxed module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-relaxed.

%prep
%setup -q -n pytest-relaxed-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytester,pytest_relaxed"
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytester,pytest_relaxed" \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/pytest_relaxed
%{py_sitescriptdir}/pytest_relaxed-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-relaxed
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/pytest_relaxed
%{py3_sitescriptdir}/pytest_relaxed-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
