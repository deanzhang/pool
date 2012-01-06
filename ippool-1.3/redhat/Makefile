# Override one or more of the following to build RPM source and binary packages
ARCH=	i686
VER=	1.3
REL=	1
PPPVER=	2.4.4
TARGZ=	/tmp/ippool-$(VER).tar.gz
SPEC=	ippool.spec
AUTHOR=	$(shell whoami)
DATE=	$(shell date '+%a %b %d %Y')
REDHAT=	/usr/src/redhat
DIST=	fc7

.PHONY:	spec rpm

all:	spec rpm

clean:
	-$(RM) $(wildcard *.rpm) ippool-$(VER)-$(REL).spec

spec:
	@if [ ! -e $(TARGZ) ]; then \
		echo "$(TARGZ) not found. Aborting." ;\
		echo "Use make TARGZ=<file> to point to the Ippool release tarball" ;\
	fi
	cp $(SPEC) ippool-1.spec
	cat ippool-1.spec | sed -e 's/%%VER%%/${VER}/g' > ippool-2.spec
	mv -f ippool-2.spec ippool-1.spec
	cat ippool-1.spec | sed -e 's/%%REL%%/${REL}/g' > ippool-2.spec
	mv -f ippool-2.spec ippool-1.spec
	cat ippool-1.spec | sed -e 's/%%PPPVER%%/${PPPVER}/g' > ippool-2.spec
	mv -f ippool-2.spec ippool-1.spec
	cat ippool-1.spec | sed -e 's/%%AUTHOR%%/$(AUTHOR)/g' > ippool-2.spec
	mv -f ippool-2.spec ippool-1.spec
	cat ippool-1.spec | sed -e 's/%%DATE%%/$(DATE)/g' > ippool-2.spec
	mv -f ippool-2.spec ippool-1.spec
	mv -f ippool-1.spec ippool-$(VER)-$(REL).spec

rpm:
	cp ippool-$(VER)-$(REL).spec $(REDHAT)/SPECS
	cp $(wildcard ippool-*.patch) $(REDHAT)/SOURCES
	cp $(TARGZ) $(REDHAT)/SOURCES
	cd $(REDHAT)/SPECS; rpmbuild -ba --target=$(ARCH)-linux ippool-$(VER)-$(REL).spec
	cp -v $(REDHAT)/RPMS/$(ARCH)/ippool-$(VER)-$(REL).$(ARCH).rpm ippool-$(VER)-$(REL).$(DIST).$(ARCH).rpm
	cp -v $(REDHAT)/SRPMS/ippool-$(VER)-$(REL).src.rpm ippool-$(VER)-$(REL).$(DIST).src.rpm

