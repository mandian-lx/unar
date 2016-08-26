Summary:	List and extract archives in several format
Name:		unar
Version:	1.10.1
Release:	1
License:	LGPLv2+
Group:		Archiving/Compression
URL:		https://unarchiver.c3.cx/commandline
Source0:	https://unarchiver.c3.cx/downloads/%{name}%{version}_src.zip

BuildRequires:	bzip2-devel
BuildRequires:	gcc-objc
BuildRequires:	gnustep-base-devel
BuildRequires:	pkgconfig(icu-uc)
#BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(zlib)

%description
Two command-line tools, unar and lsar, which can be used to extract and list
file archives in several format including RARv5.

%files
%{_bindir}/lsar
%{_bindir}/unar
%{_mandir}/man1/*.1*
%{_datadir}/bash-completion/
%doc The\ Unarchiver/README.md
%doc The\ Unarchiver/License.txt

%prep
%setup -qc
# FIXME: gcc is still in use here!
#sed -i -e "{	s|OBJCC = gcc|OBJCC ?= clang -ObjC|g
#		s|CC = gcc|CC ?= clang|g
#		s|CXX = g++|CXX ?= clang++|g
#	    }" The\ Unarchiver/XADMaster/Makefile.linux
#sed -i -e "{	s|OBJCC = gcc|OBJCC ?= clang -ObjC|g
#		s|CC = gcc|CC ?= clang|g
#		s|CXX = g++|CXX ?= clang++|g
#	    }" The\ Unarchiver/UniversalDetector/Makefile.linux

sed -i -e "/_NATIVE_OBJC_EXCEPTIONS/d" The\ Unarchiver/XADMaster/Makefile.linux
sed -i -e "/_NATIVE_OBJC_EXCEPTIONS/d" The\ Unarchiver/UniversalDetector/Makefile.linux

# fix spurious-executable-perm
find . -name "*.c" -or -name "*.h" -exec chmod 0644 '{}' \;

%build
export OBJCFLAGS=" %{optflags}"
%setup_compile_flags
%make -C The\ Unarchiver/XADMaster -f Makefile.linux

%install
# binaries
install -dm 0755 %{buildroot}%{_bindir}/
install -pm 0755 The\ Unarchiver/XADMaster/unar %{buildroot}%{_bindir}/
install -pm 0755 The\ Unarchiver/XADMaster/lsar %{buildroot}%{_bindir}/

# manpage
install -dm 0755 %{buildroot}%{_mandir}/man1/
install -pm 0644 The\ Unarchiver/Extra/*.1 %{buildroot}%{_mandir}/man1/

# bash-completion
install -dm 0755 %{buildroot}%{_datadir}/bash-completion/completions/
install -pm 0644 The\ Unarchiver/Extra/lsar.bash_completion %{buildroot}%{_datadir}/bash-completion/completions/lsar
install -pm 0644 The\ Unarchiver/Extra/unar.bash_completion %{buildroot}%{_datadir}/bash-completion/completions/unar

