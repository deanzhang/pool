
# BEGIN CONFIGURABLE SETTINGS

ifdef PPPD_SRCDIR
CFLAGS.ppp=	-I$(PPPD_SRCDIR)/include -I$(PPPD_SRCDIR)/pppd
endif
ifndef PPPD_LIBDIR
PPPD_LIBDIR=	$(SYS_LIBDIR)/pppd/$(PPPD_VERSION)
endif

# END CONFIGURABLE SETTINGS

CFLAGS	+= -g -I.. -I/usr/include/pppd $(CFLAGS.pppd) -fPIC
LDFLAGS	+= -shared

all:	ippool.so

ippool.so: ippool.c
	$(CC) -o $@ $(LDFLAGS) $(CFLAGS) -D_linux_=1 ippool.c ../ippool_rpc_client.o ../ippool_rpc_xdr.o

install: ippool.so
	$(INSTALL) -d $(DESTDIR)$(PPPD_LIBDIR)
	$(INSTALL) ippool.so $(DESTDIR)$(PPPD_LIBDIR)

clean:
	-rm -rf *.o *.so
