%global package_speccommit b87e617cddc383b9e23b077c440a16eed660d4bb
%global usver 7.14.76
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 7.14.76
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
Release: %{?xsrel}%{?dist}
License: GPL
Group: System Environment/Kernel
%{?_cov_buildrequires}
Requires: %{name}-%{modules_package} = %{version}-%{release}
Source0: qlogic-netxtreme2-7.14.76.tar.gz

%description
This package contains the Qlogic NetXtreme II iSCSI (bnx2i), 1-Gigabit (bnx2) and 10-Gigabit (bnx2x) ethernet drivers.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{__make} KVER=%{kernel_version} %{build_defs}

%install
%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
echo 'options bnx2x num_vfs=0' > %{name}.conf
%{__install} %{name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man4
%{__install} -d %{buildroot}/lib/modules/%{kernel_version}/updates
%{?_cov_wrap} %{__make} PREFIX=$RPM_BUILD_ROOT KVER=%{kernel_version} %{build_defs} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DRV_DIR=%{module_dir} DEPMOD=/bin/true install
[ %{module_dir} != updates ] && %{__mv} %{buildroot}/lib/modules/%{kernel_version}/updates/bnx2fc.ko %{buildroot}/lib/modules/%{kernel_version}/%{module_dir}

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%{?_cov_install}

%files

%package %{modules_package}
Summary: %{vendor_name} %{driver_name} device drivers
Group: System Environment/Kernel
BuildRequires: kernel-devel, bc
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

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 7.14.76-2
- CP-38416: Enable static analysis

* Thu Jan 13 2022 Deli Zhang <deli.zhang@citrix.com> - 7.14.76-1
- CP-37627: Upgrade qlogic-netxtreme2 driver to version 7.14.76

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 7.14.53-2
- CP-35517: Fix build for koji

* Thu Dec 20 2018 Deli Zhang <deli.zhang@citrix.com> - 7.14.53-1
- CP-30078: Upgrade netXtreme2 driver to version 7.14.53

* Mon Oct 23 2017 Simon Rowe <simon.rowe@citrix.com> - 7.14.29.1-1
- UPD-107: update netxtreme2 driver to 7.14.29.1 (QL-643)

