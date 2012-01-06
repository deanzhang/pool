
.PHONY:			all clean distclean install subdirs-all

all:			

clean:

distclean:		clean

TAGS:
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) $@; done
			etags -t $(wildcard *.c) $(wildcard *.h)

install:		all
			@for d in $(SUBDIRS); do $(MAKE) -C $$d $(MFLAGS) $@; if [ $$? -ne 0 ]; then exit 1; fi; done

BANNER=			@echo "----------------------------------------------------------------------------"
TCLSH=			tclsh all.tcl -preservecore 3 -verbose bps -tmpdir ./results -outfile $@.result

.PHONY:			test-setup test-postprocess test-ippool

test:			test-setup test-ippool test-postprocess

test-setup:
			@if [ -d ./results ]; then rm -fr ./results; fi
			@mkdir ./results

test-ippool:	
			$(BANNER)
			@$(TCLSH) -constraints "ipPool"

test-postprocess:	
			$(BANNER)
			@(failed=`grep FAILED results/*.result | wc -l`; \
			let failed2=failed/2 ;\
			passed=`grep PASSED results/*.result | wc -l`; \
			echo "TEST SUMMARY: $$passed tests PASSED, $$failed2 tests FAILED" ;\
			exit $$failed2)

