Summary:	Terminates connections for idle users.
Summary(pl):	Przerywa połączenia bezczynnych użytkowników.
Name:		autolog
Version:	0.34
Release:	3
License:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/Admin/idle/%{name}-%{version}.tgz
Patch0:		autolog-0.34.debian.diff
Requires:	/etc/crontab.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Autolog is a program to automatically log off users who are idle for a
specified amount of time. A configuration file allows you to specify
different idle times and logout rules for different users, groups, tty
lines, etc.

%description -l pl
Autolog to program automatycznie wylogowujący użytkowników, którzy nie
korzystają przez określony czas z terminala. Plik konfiguracyjny
pozwala na określenie czasów oraz reguł postępowania dla różnych
użytkowników, grup, lini tty itp.

%prep
%setup -q
%patch -p1

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr/sbin,usr/share/man/{man8,man5},etc/crontab.d}

install autolog $RPM_BUILD_ROOT%{_sbindir}
install crontab $RPM_BUILD_ROOT/etc/crontab.d/%{name}
install autolog.8 $RPM_BUILD_ROOT%{_mandir}/man8
install autolog.conf $RPM_BUILD_ROOT%{_sysconfdir}
install autolog.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* README 

%post
if test -r /var/run/crond.pid; then
	/etc/rc.d/init.d/crond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to activate autolog."
fi

%postun
if test -r /var/run/crond.pid; then
	/etc/rc.d/init.d/crond restart >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(700,root,root) %{_sbindir}/autolog
%attr(700,root,root) /etc/crontab.d/autolog
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/autolog.conf
%{_mandir}/man8/*
