# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free

Name:           jna-posix
Summary:        Java POSIX emulation layer
Url:            https://svn.codehaus.org/jruby-contrib/trunk/jna-posix/
Version:        0.6
Release:        %mkrel 2.0.1
Epoch:          0
License:        CPL or GPL or LGPL
Group:          Development/Java
Source0:        jna-posix-0.6.tar.gz
# svn export https://svn.codehaus.org/jruby-contrib/tags/jna-posix/0.6/ jna-posix-0.6

Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Patch0:         %{name}-pom.patch

BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-rpmbuild > 0:1.5.0
BuildRequires:  jna
BuildRequires:  maven2
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire

Requires:  java >= 0:1.5.0
Requires:  jna

Requires(post):    jpackage-utils >= 0:1.7.4
Requires(postun):  jpackage-utils >= 0:1.7.4

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
jna-posix is a lightweight cross-platform POSIX emulation
layer for Java, written in Java and leveraging the JNA
library.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
chmod -R go=u-w *
%remove_java_binaries
%patch0 -b .sav0

cp %{SOURCE1} settings.xml

%build
export JAVA_HOME=%{_jvmdir}/java-rpmbuild

sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

export SETTINGS=$(pwd)/settings.xml

mvn-jpp \
        -e \
        -s $SETTINGS \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

%add_to_maven_depmap org.jruby.ext.posix %{name} %{version} JPP %{name}
install -m 644 pom.xml \
   $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
install -m 644 target/%{name}-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root)
%{_javadir}/*.jar
%{_datadir}/maven2/poms
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

