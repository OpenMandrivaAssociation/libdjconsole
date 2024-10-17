%define lib_major 0
%define lib_name %mklibname djconsole %{lib_major}
%define devel_name %mklibname djconsole -d

Name:		libdjconsole
Summary:	Libdjconsole - Support for hardware dj consoles
Version:	0.1.3
Release:	6
License:	LGPL
Group:		System/Libraries
URL:		https://djplay.sourceforge.net/
Source:		%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libusb)
Requires:	%{lib_name} = %{version}-%{release}

%description
libdjconsole - Support for hardware dj consoles

%files
%dir %_datadir/libdjconsole
%{_datadir}/libdjconsole/*
%{_sysconfdir}/udev/rules.d/45-hpdjconsole.rules

#--------------------------------------------------------------------

%package -n %{lib_name}
Summary:	Libdjconsole - Support for hardware dj consoles
Group:		System/Libraries

%description -n %{lib_name}
libdjconsole - Support for hardware dj consoles

%files -n %{lib_name}
%{_libdir}/libdjconsole.so.%{lib_major}*


#--------------------------------------------------------------------

%package -n %{devel_name}
Summary:	Development files for Libdjconsole
Group:		Development/C++
Provides:	%{name}-devel
Requires:	%{lib_name} = %{version}-%{release}

%description -n %{devel_name}
libdjconsole - Support for hardware dj consoles

%files -n %{devel_name}
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

#--------------------------------------------------------------------

%prep
%setup -q

%__sed -i -e 's|Libs: -L${libdir} -ldjconsole|Libs: -L${libdir} -ldjconsole -lstdc++ -lusb|g' \
	libdjconsole.pc.in

%build
export CFLAGS="%{optflags}"

aclocal
libtoolize --copy --force
autoreconf

%configure2_5x \
	--enable-static=no \
	--enable-threads

%make

%install
%makeinstall_std

# Fix pkgconfig file
sed -i "s,-ldjconsole,-ldjconsole -lusb,g" %{buildroot}%{_libdir}/pkgconfig/libdjconsole.pc
sed -i "s,^libdir=.*,libdir=%{_libdir},g" %{buildroot}%{_libdir}/pkgconfig/libdjconsole.pc

%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-4mdv2011.0
+ Revision: 620095
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Götz Waschk <waschk@mandriva.org> 0.1.3-3mdv2010.0
+ Revision: 439070
- rebuild for new libusb

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Mon Sep 01 2008 Emmanuel Andry <eandry@mandriva.org> 0.1.3-1mdv2009.0
+ Revision: 278582
- fix group
- New version
- use autotools and libtoolize
- apply devel policy
- check major
- only package libs in versionned lib package

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix summary-not-capitalized
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri May 04 2007 Helio Chissini de Castro <helio@mandriva.com> 0.1.2-2mdv2008.0
+ Revision: 22535
- Fix pkgconfig for build in x86_64

* Fri May 04 2007 Helio Chissini de Castro <helio@mandriva.com> 0.1.2-1mdv2008.0
+ Revision: 22470
- First release. This is for all music hardware control freaks like me having fun \!
- import libdjconsole-0.1.2-1mdv2008.0


