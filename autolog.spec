Summary:	Terminates connections for idle users
Summary(pl):	Przerywa połączenia bezczynnych użytkowników
Name:		autolog
Version:	0.40
Release:	3
License:	GPL
Group:		Daemons
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/admin/idle/%{name}-%{version}.tar.gz
# Source0-md5:	bcca87156acfdce9171acc90b35f9d0d
Source1:	%{name}.init
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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
użytkowników, grup, linii tty itp.

%prep
%setup -q

%build
# Remove stale binaries
%{__make} clean

%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/rc.d/init.d,/var/log}

install autolog $RPM_BUILD_ROOT%{_sbindir}
install autolog.conf $RPM_BUILD_ROOT%{_sysconfdir}
install autolog.8.gz $RPM_BUILD_ROOT%{_mandir}/man8
install autolog.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

touch $RPM_BUILD_ROOT/var/log/autolog.log

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
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man?/*
%attr(640,root,root) %ghost /var/log/autolog.log
