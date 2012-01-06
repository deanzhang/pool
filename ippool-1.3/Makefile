
# BEGIN CONFIGURABLE SETTINGS

# Define USE_DMALLOC to enable dmalloc memory debugging
# USE_DMALLOC=		y

# Define to include test code. This must be defined to run the
# regression tests
# IPPOOL_TEST=		y

# Define to compile in debug code. Also makes default trace flags
# enable all messages
# IPPOOL_DEBUG=		y

# Points to pppd install. 
# By default, pppd headers are assumed to be in /usr/include/pppd. but 
# can be pointed to a local pppd source tree if desired.
PPPD_VERSION=		2.4.4
# PPPD_SRCDIR=		/usr/local/src/ppp-2.4.4
# PPPD_LIBDIR=		/usr/lib/pppd/2.4.4

# Points to readline install root. READLINE_DIR should have lib/ & include/ subdirs
# If not defined, readline is assumed to be installed in the standard places that
# the compiler looks.
READLINE_DIR=		

# For cross-compiling
CROSS_COMPILE=

# END CONFIGURABLE SETTINGS

AS		= $(CROSS_COMPILE)as
LD		= $(CROSS_COMPILE)ld
CC		= $(CROSS_COMPILE)gcc
AR		= $(CROSS_COMPILE)ar
NM		= $(CROSS_COMPILE)nm
STRIP		= $(CROSS_COMPILE)strip
INSTALL		= $(CROSS_COMPILE)install

ifneq ($(READLINE_DIR),)
READLINE_LDFLAGS=	-L $(READLINE_DIR)/lib
READLINE_CFLAGS=	-I $(READLINE_DIR)/include
endif

ARCH=$(shell uname -p)
ifeq ($(ARCH),x86_64)
SYS_LIBDIR=/usr/lib64
else
SYS_LIBDIR=/usr/lib
endif

export KERNEL_SRCDIR PPPD_VERSION PPPD_SRCDIR PPPD_LIBDIR KERNEL_VERSION READLINE_LDFLAGS READLINE_CFLAGS
export CROSS_COMPILE AS LD CC AR NM STRIP OBJCOPY OBJDUMP INSTALL SYS_LIBDIR

#
SUBDIRS=		usl cli pppd test doc

PROGS.sbin=		ippoold
PROGS.bin=		ippoolconfig

IPPOOL_RPC_STEM=	ippool_rpc

RPC_FILES=		$(IPPOOL_RPC_STEM)_server.c $(IPPOOL_RPC_STEM)_client.c $(IPPOOL_RPC_STEM)_xdr.c $(IPPOOL_RPC_STEM).h

IPPOOLD_SRCS.c=		ippool_main.c ippool_api.c ippool_impl.c ippool_test.c

IPPOOLD_SRCS.h=		ippool_api.h ippool_private.h

ifeq ($(IPPOOL_TEST),y)
CPPFLAGS.ippooltest=	-DIPPOOL_TEST
endif

IPPOOLCONFIG_SRCS.c=	ippool_config.c

IPPOOLD_SRCS.o=		$(IPPOOLD_SRCS.c:%.c=%.o) $(IPPOOL_RPC_STEM)_server.o $(IPPOOL_RPC_STEM)_xdr.o
IPPOOLCONFIG_SRCS.o=	$(IPPOOLCONFIG_SRCS.c:%.c=%.o) $(IPPOOL_RPC_STEM)_client.o $(IPPOOL_RPC_STEM)_xdr.o

ifeq ($(USE_DMALLOC),y)
CPPFLAGS.dmalloc=	-DIPPOOL_DMALLOC
LIBS.dmalloc=		-ldmalloc
export USE_DMALLOC
endif

CPPFLAGS=		$(CPPFLAGS.ippooltest)
CFLAGS=			-I. -Iusl -Icli -MMD -Wall -g $(CPPFLAGS) $(CPPFLAGS.dmalloc)
LDFLAGS.ippoold=	-Wl,-E -L. -Lusl -lusl -lnsl -ldl $(LIBS.dmalloc) -lc
LDFLAGS.ippoolconfig=	-Lcli -lcli -lreadline -lcurses -lnsl $(LIBS.dmalloc) -lc

OPT_CFLAGS?=		-O

ifeq ($(IPPOOL_DEBUG),y)
CFLAGS.optimize=	-g
CFLAGS.optimize+=	-DDEBUG
else
CFLAGS.optimize=	$(OPT_CFLAGS)
endif
export CFLAGS.optimize

CFLAGS+=		$(CFLAGS.optimize)

RPCGENFLAGS=		-N -M -C -L

.PHONY:			all clean distclean install subdirs-all

all:			generated-files $(IPPOOL_RPC_STEM)_xdr.o $(IPPOOL_RPC_STEM)_client.o \
			subdirs-all $(PROGS.sbin) $(PROGS.bin)

# Compile without -Wall because rpcgen-generated code is full of warnings
$(IPPOOL_RPC_STEM)_xdr.o:	$(IPPOOL_RPC_STEM)_xdr.c
			$(CC) -I. -MMD -g -c -w $(CPPFLAGS) $(CFLAGS.optimize) $<

$(IPPOOL_RPC_STEM)_client.o:	$(IPPOOL_RPC_STEM)_client.c
			$(CC) -I. -MMD -g -c -w $(CPPFLAGS) $(CFLAGS.optimize) $<

$(IPPOOL_RPC_STEM)_server.o:	$(IPPOOL_RPC_STEM)_server.c
			$(CC) -I. -MMD -g -c -w $(CPPFLAGS) $(CFLAGS.optimize) $<

$(IPPOOL_RPC_STEM)_xdr.c:	$(IPPOOL_RPC_STEM).x
			-$(RM) $@
			rpcgen $(RPCGENFLAGS) -c -o $@ $<

$(IPPOOL_RPC_STEM)_server.c:	$(IPPOOL_RPC_STEM).x
			-$(RM) $@ $@.tmp
			rpcgen $(RPCGENFLAGS) -m -o $@.tmp $<
			cat $@.tmp | sed -e 's/switch (rqstp->rq_proc) {/if (ippool_api_rpc_check_request(transp) < 0) return; switch (rqstp->rq_proc) {/' > $@

$(IPPOOL_RPC_STEM)_client.c:	$(IPPOOL_RPC_STEM).x
			-$(RM) $@
			rpcgen $(RPCGENFLAGS) -l -o $@ $<

$(IPPOOL_RPC_STEM).h:	$(IPPOOL_RPC_STEM).x
			-$(RM) $@
			rpcgen $(RPCGENFLAGS) -h -o $@ $<

.PHONY:			generated-files plugins clean distclean

generated-files:	$(RPC_FILES)

subdirs-all:
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) EXTRA_CFLAGS="$(CPPFLAGS)" all; if [ $$? -ne 0 ]; then exit 1; fi; done

clean:
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) $@; if [ $$? -ne 0 ]; then exit 1; fi; done
			-$(RM) $(IPPOOLD_SRCS.o) $(IPPOOLCONFIG_SRCS.o) $(PROGS.sbin) $(PROGS.bin) $(RPC_FILES)
			-$(RM) $(wildcard *.d)

distclean:		clean
			-$(RM) TAGS

TAGS:
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) $@; done
			etags -t $(wildcard *.c) $(wildcard *.h)

ippoold:		$(IPPOOLD_SRCS.o)
			$(CC) -o $@ $^ $(LDFLAGS.ippoold)

ippoolconfig:		$(IPPOOLCONFIG_SRCS.o)
			$(CC) -o $@ $^ $(LDFLAGS.ippoolconfig)

%.o:	%.c
			$(CC) -c $(CFLAGS) $< -o $@

install:		all
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) $@; if [ $$? -ne 0 ]; then exit 1; fi; done
			install -d $(DESTDIR)/usr/sbin
			install $(PROGS.sbin) $(DESTDIR)/usr/sbin
			install -d $(DESTDIR)/usr/bin
			install $(PROGS.bin) $(DESTDIR)/usr/bin
			install -d $(DESTDIR)$(SYS_LIBDIR)/ippool
			install -m 0644 ippool_rpc.x $(DESTDIR)$(SYS_LIBDIR)/ippool/ippool_rpc.x

sinclude		$(wildcard *.d) /dev/null
