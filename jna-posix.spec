Name:           jna-posix
Version:        0.5
Release:        %mkrel 0.3.1
Summary:        POSIX APIs for Java

Group:          Development/Java
License:        CPL or GPLv2+ or LGPLv2+
URL:            http://jruby.codehaus.org/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball: (0.5 was pulled from r139)
#   svn export http://svn.codehaus.org/jruby-contrib/trunk/jna-posix jna-poisx
#   tar -cjf jna-posix.tar.bz2 jna-posix/
Source0:        %{name}.tar.bz2
# The custom build.xml is just a simplified version of the stock
# build.xml. I did not include the test/cleanup sections, so it should
# be very small and understandable. (I used build.xml rather than the
# package's pom.xml (maven) because it requires maven-wagon's WebDAV
# component, something Fedora doesn't currently have.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=442641
Source1:        %{name}-build.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-rpmbuild >= 1.5
BuildRequires:  jna
BuildRequires:  jpackage-utils
BuildRequires:  junit

Requires:       java >= 1.5
Requires:       jpackage-utils
Requires:       jna


%description
Common cross-project/cross-platform POSIX APIs for Java.


%prep
%setup -q -n %{name}
rm -f build.xml
cp %{SOURCE1} build.xml

rm lib/*.jar


%build
export CLASSPATH=$(build-classpath junit jna)
%ant


%install
rm -rf $RPM_BUILD_ROOT

# JAR files
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/%{name}-%{version}.jar \
       $RPM_BUILD_ROOT%{_javadir}/%{name}.jar


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%doc LICENSE.txt README.txt
