Summary:	Library for reading and writing YAML in scripting languages
Summary(pl.UTF-8):	Biblioteka do odczytu i zapisu YAML-a w językach skryptowych
Name:		syck
Version:	0.55
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	http://rubyforge.org/frs/download.php/4492/%{name}-%{version}.tar.gz
# Source0-md5:	a57b7c46d81170b9318e2f384f77910c
Patch0:		%{name}-shared.patch
URL:		http://whytheluckystiff.net/syck/
BuildRequires:	python-devel >= 1:2.3
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Syck is an extension for reading and writing YAML swiftly in popular
scripting languages. As Syck loads the YAML, it stores the data
directly in your language's symbol table. This means speed. This means
power. This means Do not disturb Syck because it is so focused on the
task at hand that it will slay you mortally if you get in its way.

%description -l pl.UTF-8
Syck to rozszerzenie do szybkiego odczytu i zapisu YAML-a w
popularnych językach skryptowych. Po wczytaniu YAML-a Syck zapisuje
dane bezpośrednio do tablicy symboli używanego języka. To oznacza
szybkość. To oznacza potęgę. To oznacza, że nie należy
przeszkadzać Syckowi, ponieważ tak skupia się na własnym zadaniu,
że zabije, jeśli wejdziemy mu w drogę.

%package devel
Summary:	Header files for syck library
Summary(pl.UTF-8):	Pliki nag��wkowe biblioteki syck
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for syck library.

%description devel -l pl.UTF-8
Pliki nag��wkowe biblioteki syck.

%package static
Summary:	Static syck library
Summary(pl.UTF-8):	Statyczna biblioteka syck
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static syck library.

%description static -l pl.UTF-8
Statyczna biblioteka syck.

%package -n python-syck
Summary:	Python bindings for syck library
Summary(pl.UTF-8):	Pythonowy interfejes do biblioteki syck
Group:		Libraries/Python
#Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python

%description -n python-syck
Python bindings for syck library.

%description -n python-syck -l pl.UTF-8
Pythonowy interfejs do biblioteki syck.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -fPIC"

cd ext/python
env CFLAGS="%{rpmcflags} -fPIC" python setup.py build
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ext/python
python -- setup.py install \
        --root=$RPM_BUILD_ROOT \
	--install-purelib=%{py_sitedir} \
	--install-platlib=%{py_sitescriptdir} \
	--install-scripts=%{py_sitescriptdir} \
        --optimize=2

install -d $RPM_BUILD_ROOT%{py_sitedir}
install $RPM_BUILD_ROOT%{py_sitescriptdir}/syck.so $RPM_BUILD_ROOT%{py_sitedir}

find $RPM_BUILD_ROOT%{py_sitescriptdir} -name \*.py | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.BYTECODE RELEASE CHANGELOG tests
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files -n python-syck
%defattr(644,root,root,755)
%doc ext/python/tests
%{py_sitescriptdir}/*
%{py_sitedir}/*
