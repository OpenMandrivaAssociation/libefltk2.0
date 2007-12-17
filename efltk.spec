%define cvsversion 1

%define name libefltk
%define filename efltk
%define version 2.0.6

%if %cvsversion
%define release %mkrel 0.%{cvsver}.1
%elseif
%define release %mkrel 1
%endif

%define pakdir %{filename}-%{version}
%define date %(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%define cvsver 20060330

%define major 2.0
%define libname %mklibname %{filename} %major
%define libnamedev %mklibname %{filename} %major -d


Name: 		%{libname}
Version: 	%{version}
Release: 	%{release}
%if %cvsversion
Source:         %{filename}-%{cvsver}.tar.bz2
%elseif
Source: 	%{filename}-%{version}.tar.bz2
%endif

Summary:	A stable, small and fast cross-platform GUI ToolKit
URL: 		http://ede.sourceforge.net
License: 	LGPL
Group: 		System/Libraries

BuildRequires: 	gettext
Provides:	efltk

%description
Extended Fast Light Toolkit (eFLTK)
is a cross-platform C++ GUI toolkit for UNIX®/Linux® (X11), 
Microsoft® Windows®, and MacOS® X. eFLTK provides modern GUI 
functionality without the bloat and supports 3D graphics via 
OpenGL® and its built-in GLUT emulation. It is currently maintained 
by a small group of developers across the world with a central 
repository on SourceForge.

%package -n %{libnamedev}
Summary: Header files and libraries for developing apps which will eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		Development/C++
Requires: 	%{name} = %{version}
Provides:	efltk-devel

%description -n %{libnamedev}
The efltk-devel package contains the header files and libraries needed
to develop programs that use the eFLTK libraries.

%package -n efltk-themes
Summary: Themes for eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		System/Libraries
Requires: 	%{name} = %{version}

%description -n efltk-themes
This package contains themes which can be used with eFLTK. Note: in
version 2.0.2 these themes don't seem to work...

%package -n efluid
Summary: 	GUI designer for EDE / eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		Development/C++
Requires: 	%{name} = %{version}
#Requires: 	%{name}-devel = %{version}

%description -n efluid
Efluid is a WYSIWYG GUI designer for the eFLTK toolkit. It can generate 
C++ code and export strings for translation in gettext format. It is 
still under development which means that it doesn't support some of the 
features of eFLTK.

%package -n ecalc
Summary: Scientific calculator for EDE
Version: 	%{version}
Release: 	%{release}
Group: 		Graphical desktop/Other
Requires: 	%{name} = %{version}

%description -n ecalc
Ecalc is a scientific calculator for the Equinox Desktop Environment, made as
a demo of eFLTK toolkit.

%package -n etranslate
Summary: Program interface translation tool for EDE
Version: 	%{version}
Release: 	%{release}
Group: 		Development/Other
Requires: 	%{name} = %{version}

%description -n etranslate
Etranslate is an editor of gettext (.PO) files. This format is commonly used 
in open-source projects such as EDE to enable localization of programs.


%prep
%if %cvsversion
%setup -q -n %{filename}-%{cvsver}
%elseif
%setup -q -n %{filename}
%endif

%build

%if %cvsversion
autoconf
%endif

%configure --enable-xft

make

%install

# Why is this needed?
install -d $RPM_BUILD_ROOT/%{_prefix}
install -d $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_includedir}
install -d $RPM_BUILD_ROOT/%{_libdir}

%makeinstall

# I have a problem with locale
rm -fr $RPM_BUILD_ROOT/%{_datadir}/locale/

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/efltk-config

%find_lang %name

%clean
rm -fr $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root)
%{_libdir}/lib*.so*
# %{_datadir}/locale/*/*/* - this is now dealt with find_lang

%files -n efluid
%defattr(-, root, root)
%{_bindir}/efluid

%files -n ecalc
%defattr(-, root, root)
%{_bindir}/ecalc

%files -n etranslate
%defattr(-, root, root)
%{_bindir}/etranslate

%files -n efltk-themes
%defattr(-, root, root)
%{_libdir}/fltk/*.theme


%files -n %{libnamedev}
%defattr(-, root, root)
%doc doc/*
%defattr(-, root, root)
%{_includedir}/*
%multiarch %{_bindir}/multiarch-*-linux/*
%{_bindir}/*
#%{_libdir}/*.a
#%{_libdir}/*.la

