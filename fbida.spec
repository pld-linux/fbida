#
# TODO: package thumbnail.cgi (in %{_libdir}/cgi-bin?)
#
# Conditional build:
%bcond_without	curl	# without URL support
%bcond_without	exif	# without EXIF tags support
%bcond_without	gif	# without GIF images support
%bcond_without	lirc	# without LIRC control support
%bcond_without	motif	# don't build (Motif-based) ida
%bcond_without	pcd	# without PCD images support
%bcond_without	png	# without PNG images support
%bcond_without	sane	# without SANE scanning support (in ida)
%bcond_without	tiff	# without TIFF images support
#
%if %{without motif}
# SANE used only in ida
%undefine	with_sane
%endif
Summary:	fbida - a few applications for viewing and editing images
Summary(pl):	fbida - kilka aplikacji do ogl±dania i edycji obrazków
Name:		fbida
Version:	2.01
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://dl.bytesex.org/releases/fbida/%{name}-%{version}.tar.gz
# Source0-md5:	40330052742c3c9144b03365d36fbea0
Patch0:		%{name}-fbgs.patch
Patch1:		%{name}-config-noforce.patch
Patch2:		%{name}-desktop.patch
URL:		http://linux.bytesex.org/fbida/
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	libexif-devel >= 1:0.6.9
BuildRequires:	libjpeg-devel
%{?with_pcd:BuildRequires:	libpcd-devel >= 1:1.0.1}
%{?with_png:BuildRequires:	libpng-devel}
%{?with_lirc:BuildRequires:	lirc-devel}
%{?with_tiff:BuildRequires:	libtiff-devel}
%{?with_gif:BuildRequires:	libungif-devel}
# acc. to README lesstif is not sufficient
%{?with_motif:BuildRequires:	openmotif-devel >= 2.0}
BuildRequires:	pkgconfig
%{?with_sane:BuildRequires:	sane-backends-devel}
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults

%description
The fbida project contains a few applications for viewing and editing
images, with the main focus being photos. The applications are:
- fbi - image viewer for the Linux framebuffer console
- fbgs - wrapper script for viewing PS/PDF files using fbi
- ida - Motif-based application for viewing images
- exiftran - command-line tool to do lossless transformations of JPEG
  images
- thumbnail.cgi - small and fast CGI program to extract EXIF
  thumbnails from JPEG images and send them to the web browser

%description -l pl
Projekt fbida zawiera kilka aplikacji do ogl±dania i edycji obrazków,
g³ównie przeznaczonych dla zdjêæ. Te aplikacje to:
- fbi - przegl±darka dla linuksowej konsoli z framebufferem
- fbgs - skrypt do ogl±dania plików PS/PDF przy u¿yciu fbi
- ida - oparta na Motifie aplikacja do ogl±dania obrazków
- exiftran - dzia³aj±ce z linii poleceñ narzêdzie do wykonywania
  bezstratnych przekszta³ceñ obrazków JPEG
- thumbnail.cgi - ma³y i szybki program CGI do wyci±gania miniaturek
  EXIF z obrazków JPEG i wysy³ania ich do przegl±darki WWW

%package -n fbi
Summary:	Linux FrameBuffer Imageviewer
Summary(pl):	Przegl±darka obrazków dla linuksowego framebuffera
Group:		Applications/Graphics

%description -n fbi
This is a image viewer for linux framebuffer devices. It supports
PhotoCD, JPEG and PPM directly. GIF, TIFF and PNG are handled with the
netpbm tools, for anything else convert from the ImageMagick package
is used as external converter.

This package contains also additional utilities:
- fbgs - wrapper script for viewing PS/PDF files using fbi
- exiftran - command-line tool to do lossless transformations of JPEG
  images

%description -n fbi -l pl
To jest przegl±darka obrazków korzystaj±ca z framebuffera. Obs³uguje
bezpo¶rednio PhotoCD, JPEG i PPM; GIF, TIFF i PNG poprzez narzêdzia z
pakietu netpbm-progs; inne obrazki poprzez program convert z pakietu
ImageMagick.

Ten pakiet zawiera tak¿e dodatkowe narzêdzia:
- fbgs - skrypt do ogl±dania plików PS/PDF przy u¿yciu fbi
- exiftran - dzia³aj±ce z linii poleceñ narzêdzie do wykonywania
  bezstratnych przekszta³ceñ obrazków JPEG

%package -n ida
Summary:	Small and fast image viewer, Motif-based
Summary(pl):	Ma³a, szybka przegl±darka obrazków oparta na Motifie
Group:		X11/Applications/Graphics

%description -n ida
Ida is a small and fast image viewer, Motif-based. For people who
don't want the KDE/GNOME overhead. Some basic editing functions are
available too.

%description -n ida -l pl
Ida to ma³a i szybka przegl±darka obrazków oparta na Motifie.
Przeznaczona jest dla ludzi, którzy nie chc± narzutu KDE/GNOME.
Dostêpne jest te¿ trochê podstawowych funkcji edycyjnych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{rpmcflags}" \
%{__make} \
	CC="%{__cc}" \
	verbose=yes \
	%{!?with_pcd:HAVE_LIBPCD=no} \
	%{!?with_gif:HAVE_LIBUNGIF=no} \
	%{!?with_png:HAVE_LIBPNG=no} \
	%{!?with_tiff:HAVE_LIBTIFF=no} \
	%{!?with_sane:HAVE_LIBSANE=no} \
	%{!?with_curl:HAVE_LIBCURL=no} \
	%{!?with_lirc:HAVE_LIBLIRC=no} \
	%{!?with_motif:HAVE_MOTIF=no}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	INSTALL_BINARY=install \
	%{!?with_pcd:HAVE_LIBPCD=no} \
	%{!?with_gif:HAVE_LIBUNGIF=no} \
	%{!?with_png:HAVE_LIBPNG=no} \
	%{!?with_tiff:HAVE_LIBTIFF=no} \
	%{!?with_sane:HAVE_LIBSANE=no} \
	%{!?with_curl:HAVE_LIBCURL=no} \
	%{!?with_lirc:HAVE_LIBLIRC=no} \
	%{!?with_motif:HAVE_MOTIF=no}

%if %{with motif}
install -D desktop/ida.desktop $RPM_BUILD_ROOT%{_desktopdir}/ida.desktop
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -n fbi
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/exiftran
%attr(755,root,root) %{_bindir}/fbgs
%attr(755,root,root) %{_bindir}/fbi
%{_mandir}/man1/exiftran.1*
%{_mandir}/man1/fbgs.1*
%{_mandir}/man1/fbi.1*

%if %{with motif}
%files -n ida
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/ida
%{_mandir}/man1/ida.1*
%{_appdefsdir}/Ida
%{_desktopdir}/ida.desktop
%endif
