# TODO:
# - package thumbnail.cgi (in %{_libdir}/cgi-bin?)
#
# Conditional build:
%bcond_without	curl		# without URL support
%bcond_without	exif		# without EXIF tags support
%bcond_without	gif		# without GIF images support
%bcond_without	lirc		# without LIRC control support
%bcond_without	motif		# don't build (Motif-based) ida
%bcond_without	pcd		# without PCD images support
%bcond_without	sane		# without SANE scanning support (in ida)
%bcond_without	webp		# without WebP images support
%bcond_with	cairogl		# with Cairo-GL support (in fbpdf program)

%if %{without motif}
# SANE used only in ida
%undefine	with_sane
%endif
Summary:	fbida - a few applications for viewing and editing images
Summary(pl.UTF-8):	fbida - kilka aplikacji do oglądania i edycji obrazków
Name:		fbida
Version:	2.14
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	https://www.kraxel.org/releases/fbida/%{name}-%{version}.tar.gz
# Source0-md5:	f5475b359461d2d995bde59e13cc584f
Patch0:		%{name}-config-noforce.patch
Patch1:		%{name}-desktop.patch
URL:		https://www.kraxel.org/blog/linux/fbida/
BuildRequires:	EGL-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	cairo-devel
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0.0
# -Wno-pointer-sign
BuildRequires:	gcc >= 5:4.0
%{?with_gif:BuildRequires:	giflib-devel}
BuildRequires:	libdrm-devel
BuildRequires:	libepoxy-devel
BuildRequires:	libexif-devel >= 1:0.6.9
BuildRequires:	libjpeg-devel
%{?with_pcd:BuildRequires:	libpcd-devel >= 1:1.0.1}
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel >= 4
%{?with_webp:BuildRequires:	libwebp-devel}
%{?with_lirc:BuildRequires:	lirc-devel}
# acc. to README lesstif is not sufficient
%{?with_motif:BuildRequires:	motif-devel >= 2.0}
BuildRequires:	perl-base
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
%{?with_cairogl:BuildRequires:	pkgconfig(cairo-gl)}
BuildRequires:	poppler-glib-devel
%{?with_sane:BuildRequires:	sane-backends-devel}
BuildRequires:	util-linux
BuildRequires:	which
BuildRequires:	xorg-lib-libXpm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/share/X11/app-defaults

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

%description -l pl.UTF-8
Projekt fbida zawiera kilka aplikacji do oglądania i edycji obrazków,
głównie przeznaczonych dla zdjęć. Te aplikacje to:
- fbi - przeglądarka dla linuksowej konsoli z framebufferem
- fbgs - skrypt do oglądania plików PS/PDF przy użyciu fbi
- ida - oparta na Motifie aplikacja do oglądania obrazków
- exiftran - działające z linii poleceń narzędzie do wykonywania
  bezstratnych przekształceń obrazków JPEG
- thumbnail.cgi - mały i szybki program CGI do wyciągania miniaturek
  EXIF z obrazków JPEG i wysyłania ich do przeglądarki WWW

%package -n fbi
Summary:	Linux FrameBuffer Imageviewer
Summary(pl.UTF-8):	Przeglądarka obrazków dla linuksowego framebuffera
Group:		Applications/Graphics
Requires:	mktemp >= 1.3

%description -n fbi
This is a image viewer for linux framebuffer devices. It supports
PhotoCD, JPEG and PPM directly. GIF, TIFF and PNG are handled with the
netpbm tools, for anything else convert from the ImageMagick package
is used as external converter.

This package contains also additional utilities:
- fbgs - wrapper script for viewing PS/PDF files using fbi
- exiftran - command-line tool to do lossless transformations of JPEG
  images

%description -n fbi -l pl.UTF-8
To jest przeglądarka obrazków korzystająca z framebuffera. Obsługuje
bezpośrednio PhotoCD, JPEG i PPM; GIF, TIFF i PNG poprzez narzędzia z
pakietu netpbm-progs; inne obrazki poprzez program convert z pakietu
ImageMagick.

Ten pakiet zawiera także dodatkowe narzędzia:
- fbgs - skrypt do oglądania plików PS/PDF przy użyciu fbi
- exiftran - działające z linii poleceń narzędzie do wykonywania
  bezstratnych przekształceń obrazków JPEG

%package -n fbpdf
Summary:	Linux FrameBuffer PDF viewer
Summary(pl.UTF-8):	Przeglądarka plików PDF dla linuksowego framebuffera
Group:		Applications/Graphics

%description -n fbpdf
Linux FrameBuffer PDF viewer.

%description -n fbpdf -l pl.UTF-8
Przeglądarka plików PDF dla linuksowego framebuffera.

%package -n ida
Summary:	Small and fast image viewer, Motif-based
Summary(pl.UTF-8):	Mała, szybka przeglądarka obrazków oparta na Motifie
Group:		X11/Applications/Graphics

%description -n ida
Ida is a small and fast image viewer, Motif-based. For people who
don't want the KDE/GNOME overhead. Some basic editing functions are
available too.

%description -n ida -l pl.UTF-8
Ida to mała i szybka przeglądarka obrazków oparta na Motifie.
Przeznaczona jest dla ludzi, którzy nie chcą narzutu KDE/GNOME.
Dostępne jest też trochę podstawowych funkcji edycyjnych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{rpmcflags}" \
%{__make} \
	CC="%{__cc}" \
	verbose=yes \
	%{!?with_cairogl:HAVE_CAIRO_GL=no} \
	%{!?with_pcd:HAVE_LIBPCD=no} \
	%{!?with_gif:HAVE_LIBGIF=no} \
	%{!?with_webp:HAVE_LIBWEBP=no} \
	%{!?with_motif:HAVE_MOTIF=no} \
	%{?with_sane:HAVE_LIBSANE=yes} \
	%{?with_curl:HAVE_LIBCURL=yes} \
	%{?with_lirc:HAVE_LIBLIRC=yes}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	INSTALL_BINARY=install \
	%{!?with_cairogl:HAVE_CAIRO_GL=no} \
	%{!?with_pcd:HAVE_LIBPCD=no} \
	%{!?with_gif:HAVE_LIBGIF=no} \
	%{!?with_webp:HAVE_LIBWEBP=no} \
	%{!?with_motif:HAVE_MOTIF=no} \
	%{?with_sane:HAVE_LIBSANE=yes} \
	%{?with_curl:HAVE_LIBCURL=yes} \
	%{?with_lirc:HAVE_LIBLIRC=yes}

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

%files -n fbpdf
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fbpdf

%if %{with motif}
%files -n ida
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/ida
%{_mandir}/man1/ida.1*
%{_appdefsdir}/Ida
%{_desktopdir}/ida.desktop
%endif
