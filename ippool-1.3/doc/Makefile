
.PHONY:		all clean install

MANSRC.1=	ippoolconfig.1
MANSRC.4=	ippool_rpc.4
MANSRC.8=	ippoold.8

MANSRC=		$(MANSRC.1) $(MANSRC.4) $(MANSRC.8) 

all:		$(MANSRC:%=%.gz)

%.gz: %
		gzip --best -c $< > $@

clean:
		-$(RM) $(MANSRC:%=%.gz)

install:	all
		$(INSTALL) -d $(DESTDIR)/usr/share/man/man1
		$(INSTALL) $(MANSRC.1:%=%.gz) $(DESTDIR)/usr/share/man/man1
		$(INSTALL) -d $(DESTDIR)/usr/share/man/man4
		$(INSTALL) $(MANSRC.4:%=%.gz) $(DESTDIR)/usr/share/man/man4
		$(INSTALL) -d $(DESTDIR)/usr/share/man/man8
		$(INSTALL) $(MANSRC.8:%=%.gz) $(DESTDIR)/usr/share/man/man8


