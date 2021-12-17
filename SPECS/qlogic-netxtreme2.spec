%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name netxtreme2

%if %undefined kernel_version
%define kernel_version dummy
%endif
%if %undefined module_dir
%define module_dir updates
%endif
%if %undefined modules_suffix
%define modules_suffix modules
%endif

%define modules_package %{kernel_version}-%{modules_suffix}
%define build_defs BNX2FC_KERNEL_OVERRIDE=1 BNX2FC_SUP=-DXENSERVER DISTRO=Citrix

Summary: Qlogic NetXtreme II iSCSI, 1-Gigabit and 10-Gigabit ethernet drivers
Name: %{vendor_label}-%{driver_name}
Version: 7.14.76
Release: 1.1%{?dist}
License: GPL
Group: System Environment/Kernel
Requires: %{name}-%{modules_package} = %{version}-%{release}

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-qlogic-netxtreme2/archive?at=7.14.76&format=tgz&prefix=driver-qlogic-netxtreme2-7.14.76#/qlogic-netxtreme2-7.14.76.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-qlogic-netxtreme2/archive?at=7.14.76&format=tgz&prefix=driver-qlogic-netxtreme2-7.14.76#/qlogic-netxtreme2-7.14.76.tar.gz) = fd5406760a6d1e292fe862ba7924caff97da6e15


# XCP-ng patches
Patch1000: qlogic-netxtreme2-7.14.76-Fix-NULL-pointer-dereference.XCP-ng.patch

%description
This package contains the Qlogic NetXtreme II iSCSI (bnx2i), 1-Gigabit (bnx2) and 10-Gigabit (bnx2x) ethernet drivers.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{__make} KVER=%{kernel_version} %{build_defs}

%install
%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
echo 'options bnx2x num_vfs=0' > %{name}.conf
%{__install} %{name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man4
%{__install} -d %{buildroot}/lib/modules/%{kernel_version}/updates
%{?cov_wrap} %{__make} PREFIX=$RPM_BUILD_ROOT KVER=%{kernel_version} %{build_defs} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DRV_DIR=%{module_dir} DEPMOD=/bin/true install
[ %{module_dir} != updates ] && %{__mv} %{buildroot}/lib/modules/%{kernel_version}/updates/bnx2fc.ko %{buildroot}/lib/modules/%{kernel_version}/%{module_dir}

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%files

%package %{modules_package}
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-qlogic-netxtreme2/archive?at=7.14.76&format=tgz&prefix=driver-qlogic-netxtreme2-7.14.76#/qlogic-netxtreme2-7.14.76.tar.gz) = fd5406760a6d1e292fe862ba7924caff97da6e15
Summary: %{vendor_name} %{driver_name} device drivers
Group: System Environment/Kernel
BuildRequires: kernel-devel, bc, git
BuildRequires: gcc
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description %{modules_package}
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%post %{modules_package}
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun %{modules_package}
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans %{modules_package}
%{regenerate_initrd_posttrans}

%files %{modules_package}
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
/lib/modules/%{kernel_version}/*/*.ko
%exclude /etc/depmod.d/bnx2x.conf
%exclude %{_mandir}/man4/*

%changelog
* Fri Dec 17 2021 Gael Duperrey <gduperrey@vates.fr> - 7.14.76-1.1
- Sync with CH 8.2.1
- *** Upstream changelog ***
- * Thu Jul 8 2021 Chuntian Xu <chuntian.xu@citrix.com> - 7.14.76-1
- - CP-37167: Update netXtreme2 driver to version 7.14.76
- Drop patch partially applied upstream
- Dropped patch: qlogic-netxtreme2-Fix-NULL-pointer-dereference-in-bnx2x_del_all_vlans.backport.patch
- Add new patch to extend upstream's same fix to more devices, as in the dropped patch
- New patch: qlogic-netxtreme2-7.14.76-Fix-NULL-pointer-dereference.XCP-ng.patch

* Wed Feb 12 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.14.53-1.1
- Backport patch from kernel tree
- qlogic-netxtreme2-Fix-NULL-pointer-dereference-in-bnx2x_del_all_vlans.backport.patch

* Thu Dec 20 2018 Deli Zhang <deli.zhang@citrix.com> - 7.14.53-1
- CP-30078: Upgrade netXtreme2 driver to version 7.14.53

* Mon Oct 23 2017 Simon Rowe <simon.rowe@citrix.com> - 7.14.29.1-1
- UPD-107: update netxtreme2 driver to 7.14.29.1 (QL-643)

