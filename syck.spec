#
# TODO: php and others bindings

%define	module	rdflib

Summary:	library for reading and writing YAML in scripting languages
Name:		syck
Version:	0.45
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	http://rubyforge.org/frs/download.php/1371/%{name}-%{version}.tar.gz
# Source0-md5:	8071e1e2ee255576f025b4cef8feee62
URL:		http://whytheluckystiff.net/syck/
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table. This means speed. This means power. This means Do not
disturb Syck because it is so focused on the task at hand that it will slay
you mortally if you get in its way.

%package -n python-syck
Summary:        Python bindings for syck library
Summary(pl):    Pythonowy interfejes do biblioteki syck
Group:          Libraries/Python
#Requires:       %{name} = %{version}-%{release}
%pyrequires_eq  python

%description -n python-syck
Python bindings for syck library.

%description -n python-syck -l pl
Pythonowy interfejs do biblioteki syck


%prep
%setup

%build
%configure
%{__make}

cd ext/python
env CFLAGS="%{rpmcflags}" python setup.py build
cd ..



%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

cd ext/python
python -- setup.py install \
        --root=$RPM_BUILD_ROOT \
	--install-purelib=%{py_sitedir} \
	--install-platlib=%{py_sitescriptdir} \
	--install-scripts=%{py_sitescriptdir} \
        --optimize=2

find $RPM_BUILD_ROOT%{py_sitescriptdir} -name \*.py | xargs rm -f
%{__install} -d $RPM_BUILD_ROOT%{py_sitedir}
cp $RPM_BUILD_ROOT%{py_sitescriptdir}/syck.so $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.BYTECODE RELEASE CHANGELOG tests
%{_libdir}/*
%{_includedir}/*

%files -n python-syck
%defattr(644,root,root,755)
%doc ext/python/tests
%{py_sitescriptdir}/*
%{py_sitedir}/*
