Summary:	Terminates connections for idle users.
Summary(pl):	Przerywa po³±czenia bezczynnych u¿ytkowników.
Name:		autolog
Version:	0.34
Release:	1
Copyright:	GPL
Group:		Daemons
Group(pl):	Demony
Source:		ftp://sunsite.unc.edu/pub/Linux/system/Admin/idle/%{name}-%{version}.tgz
Patch:		autolog-0.34.debian.diff
Requires:	/etc/crontab.d
BuildRoot:	/tmp/%{version}-%{name}-buildroot

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
install -d $RPM_BUILD_ROOT/{usr/sbin,usr/man/{man8,man5},etc/crontab.d}

install autolog $RPM_BUILD_ROOT/usr/sbin
install crontab $RPM_BUILD_ROOT/etc/crontab.d/%{name}
install autolog.8 $RPM_BUILD_ROOT/usr/man/man8
install autolog.conf $RPM_BUILD_ROOT/etc
install autolog.conf.5 $RPM_BUILD_ROOT/usr/man/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(644, root, root, 755) %doc README
%attr(700, root, root) /usr/sbin/autolog
%attr(700, root, root) /etc/crontab.d/autolog
%attr(600, root, root) %config(noreplace) /etc/autolog.conf
%attr(644, root, man ) /usr/man/man8/*

%changelog
* Fri Oct 16 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- initial rpm release.
