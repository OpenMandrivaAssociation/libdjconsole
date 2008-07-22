%define lib_major 0
%define lib_name %mklibname djconsole %{lib_major}

Name: libdjconsole
Summary: Libdjconsole - Support for hardware dj consoles
Version: 0.1.2
Release: %mkrel 4
License: LGPL
Group: Development/Libraries
Source: %{name}-%{version}.tar.gz
URL: http://djplay.sourceforge.net/
BuildRequires: dbus-devel 
BuildRequires: pkgconfig
BuildRequires: hal-devel
BuildRequires: libusb-devel
BuildRequires: sed
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
libdjconsole - Support for hardware dj consoles

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
%dir %_datadir/libdjconsole
%_datadir/libdjconsole/*
%_sysconfdir/udev/rules.d/40-hpdjconsole.rules
%_libdir/libdjconsole.so.*


#--------------------------------------------------------------------

%package -n %{lib_name}-devel
Summary:  %{summary}
Group: %{group}
Provides: %name-devel
Requires: %{lib_name} = %{version}

%description -n %{lib_name}-devel
libdjconsole - Support for hardware dj consoles

%files -n %{lib_name}-devel
%defattr(-,root,root)
%_libdir/pkgconfig/*
%_libdir/*.so
%_libdir/*.la
%_includedir/*

#--------------------------------------------------------------------

%prep
%setup -q

%build
export CFLAGS="%optflags"

%configure2_5x \
    --enable-static=no 

%make

%install
make DESTDIR=%buildroot install

# Fix pkgconfig file
sed -i "s,-ldjconsole,-ldjconsole -lusb,g" %buildroot/%_libdir/pkgconfig/libdjconsole.pc
sed -i "s,^libdir=.*,libdir=%_libdir,g" %buildroot/%_libdir/pkgconfig/libdjconsole.pc

%clean
rm -rf %buildroot 

