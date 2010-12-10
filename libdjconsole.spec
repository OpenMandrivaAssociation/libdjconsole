%define lib_major 0
%define lib_name %mklibname djconsole %{lib_major}
%define devel_name %mklibname djconsole -d

Name: libdjconsole
Summary: Libdjconsole - Support for hardware dj consoles
Version: 0.1.3
Release: %mkrel 4
License: LGPL
Group: System/Libraries
Source: %{name}-%{version}.tar.gz
URL: http://djplay.sourceforge.net/
BuildRequires: dbus-devel 
BuildRequires: pkgconfig
BuildRequires: hal-devel
BuildRequires: libusb-devel
BuildRequires: sed
Requires: %{lib_name} = %{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
libdjconsole - Support for hardware dj consoles


%files
%defattr(-,root,root)
%dir %_datadir/libdjconsole
%_datadir/libdjconsole/*
%_sysconfdir/udev/rules.d/45-hpdjconsole.rules

#--------------------------------------------------------------------

%package -n %{lib_name}
Summary:  %{summary}
Group: %{group}

%description -n %{lib_name}
libdjconsole - Support for hardware dj consoles

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%_libdir/libdjconsole.so.%{lib_major}*


#--------------------------------------------------------------------

%package -n %{devel_name}
Summary:  %{summary}
Group: Development/C++
Provides: %{name}-devel
Requires: %{lib_name} = %{version}
Obsoletes: %{lib_name}-devel

%description -n %{devel_name}
libdjconsole - Support for hardware dj consoles

%files -n %{devel_name}
%defattr(-,root,root)
%_libdir/pkgconfig/*
%_libdir/*.so
%_libdir/*.la
%_includedir/*

#--------------------------------------------------------------------

%prep
%setup -q

%__sed -i -e 's|Libs: -L${libdir} -ldjconsole|Libs: -L${libdir} -ldjconsole -lstdc++ -lusb|g' \
	libdjconsole.pc.in

%build
export CFLAGS="%optflags"

aclocal
libtoolize --copy --force
autoreconf

%configure2_5x \
	--enable-static=no \
	--enable-threads

%make

%install
make DESTDIR=%buildroot install

# Fix pkgconfig file
sed -i "s,-ldjconsole,-ldjconsole -lusb,g" %buildroot/%_libdir/pkgconfig/libdjconsole.pc
sed -i "s,^libdir=.*,libdir=%_libdir,g" %buildroot/%_libdir/pkgconfig/libdjconsole.pc

%clean
rm -rf %buildroot 

