Summary: An IP address pool manager.
Name: ippool
Version: %%VER%%
Release: %%REL%%
License: GPL
Group: System Environment/daemons
URL: ftp://downloads.sourceforge.net/projects/openl2tp/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
Vendor: Katalix Systems Ltd
Packager: James Chapman <jchapman--at--katalix.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Prereq: ppp == %%PPPVER%%, readline >= 4.2, portmap
ExclusiveOS: Linux

BuildPrereq: ppp == %%PPPVER%%, readline >= 4.2, glibc >= 2.4, flex, bison

Patch0: ippool-rm_unused.patch

%description
IpPool is an IP address pool manager.

IpPool is implemented as a separate server daemon to allow any application
to use its address pools. This makes it possible to define address
pools that are shared by PPP, L2TP, PPTP etc. It may be useful in some VPN
server setups.

IpPool comes with a command line management application, ippoolconfig
to manage and query address pool status. A pppd plugin is supplied which
allows pppd to request IP addresses from ippoold.

%prep
%setup
%patch -p1 

%build
make OPT_CFLAGS="$RPM_OPT_FLAGS" \
	PPPD_VERSION=%%PPPVER%%

%install
make install DESTDIR=$RPM_BUILD_ROOT \
	PPPD_VERSION=%%PPPVER%%

%{__mkdir} -p $RPM_BUILD_ROOT/etc/rc.d/init.d $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
%{__cp} -f etc/rc.d/init.d/ippoold $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ippoold
%{__cp} -f etc/sysconfig/ippoold $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ippoold

%clean
if [ "$RPM_BUILD_ROOT" != `echo $RPM_BUILD_ROOT | sed -e s/ippool-//` ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root,-)
%doc README
%dir %{_libdir}/ippool
/usr/bin/ippoolconfig
/usr/sbin/ippoold
%{_libdir}/ippool/ippool_rpc.x
%{_libdir}/pppd/%%PPPVER%%/ippool.so
/usr/share/man/man1/ippoolconfig.1.gz
/usr/share/man/man4/ippool_rpc.4.gz
/usr/share/man/man8/ippoold.8.gz
/etc/rc.d/init.d/ippoold
/etc/sysconfig/ippoold

%changelog
* %%DATE%% James Chapman - %%VER%%

- Fix version number. Versions 1.1 and 1.2 advertised themselves as 1.0.

* Fri Mar 21 2008 James Chapman - 1.2

- Change to Debian package control file.

* Sun Feb 24 2008 James Chapman - 1.1

- Build with new USL list management code which includes memory
  barriers. This prevents gcc function order optimisations from
  causing problems.
  
- Enable compiler optimisation.

* Sun Feb 10 2008 James Chapman - 1.0

- Initial build.

