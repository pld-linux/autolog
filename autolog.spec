Summary:	Terminates connections for idle users.
Summary(pl):	Przerywa po³±czenia bezczynnych u¿ytkowników.
Name:		autolog
Version:	0.34
Release:	3
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
Source:		ftp://sunsite.unc.edu/pub/Linux/system/Admin/idle/%{name}-%{version}.tgz
Patch:		autolog-0.34.debian.diff
Requires:	/etc/crontab.d
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Autolog is a program to automatically log off users who are idle for a specified
amount of time. A configuration file allows you to specify different idle times
and logout rules for different users, groups, tty lines, etc.

%description -l pl
Autolog to program automatycznie wylogowuj±cy u¿ytkowników, którzy nie
korzystaj± przez okre¶lony czas z terminala. Plik konfiguracyjny pozwala
na okre¶lenie czasów oraz regu³ postêpowania dla ró¿nych u¿ytkowników, grup,
lini tty itp.

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
install autolog.conf $RPM_BUILD_ROOT/etc
install autolog.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* README 

%post
if test -r /var/run/crond.pid; then
	/etc/rc.d/init.d/crond stop >&2
	/etc/rc.d/init.d/crond start >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to activate autolog."
fi

%postun
if test -r /var/run/crond.pid; then
	/etc/rc.d/init.d/crond stop >&2
	/etc/rc.d/init.d/crond start >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755) 
%doc README.gz
%attr(700,root,root) %{_sbindir}/autolog
%attr(700,root,root) /etc/crontab.d/autolog
%attr(600,root,root) %config(noreplace) /etc/autolog.conf
%{_mandir}/man8/*
