Summary:	Terminates connections for idle users
Summary(pl):	Przerywa po³±czenia bezczynnych u¿ytkowników
Name:		autolog
Version:	0.40
Release:	1
License:	GPL
Group:		Daemons
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/Admin/idle/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Autolog is a program to automatically log off users who are idle for a
specified amount of time. A configuration file allows you to specify
different idle times and logout rules for different users, groups, tty
lines, etc.

%description -l pl
Autolog to program automatycznie wylogowuj±cy u¿ytkowników, którzy nie
korzystaj± przez okre¶lony czas z terminala. Plik konfiguracyjny
pozwala na okre¶lenie czasów oraz regu³ postêpowania dla ró¿nych
u¿ytkowników, grup, linii tty itp.

%prep
%setup -q

%build
# Remove stale binaries
%{__make} clean

%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}/rc.d/init.d}

install autolog $RPM_BUILD_ROOT%{_sbindir}
install autolog.conf $RPM_BUILD_ROOT%{_sysconfdir}
install autolog.8.gz $RPM_BUILD_ROOT%{_mandir}/man8
install autolog.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add autolog
if [ -f /var/lock/subsys/autolog ]; then
	/etc/rc.d/init.d/autolog restart >&2
else
	echo "Run \"/etc/rc.d/init.d/autolog start\" to activate autolog."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/autolog ]; then
		/etc/rc.d/init.d/autolog stop >&2
	fi
	/sbin/chkconfig --del autolog
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(755,root,root) %{_sbindir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/autolog.conf
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%{_mandir}/man?/*
