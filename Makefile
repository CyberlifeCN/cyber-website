DESTDIR = /
SVCDIR = $(DESTDIR)/opt/cyberlife/service/cyber-website

all:
	# nothing to do with goal: '$@'

install: uninstall
	mkdir -p $(SVCDIR)
	cp -r foo static templates *.py *.sql $(SVCDIR)
	cp -r etc $(DESTDIR)
	-@tree $(SVCDIR) || find $(SVCDIR)

uninstall:
	rm -rf $(SVCDIR)

clean:
	# nothing to do with goal: '$@'
