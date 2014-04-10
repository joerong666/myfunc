cur_dir=$(shell pwd)
depend_dir=$(HOME)/download

openssl=openssl-1.0.1e
openssl_home=$(HOME)/local/$(openssl)

py=Python-2.7.3
py_home=$(HOME)/local/$(py)

pyssl=pyOpenSSL-0.13

default:
	@echo "make [install|install-openssl|install-python|install-pyOpenssl|install-func]"

install-openssl:
	cd $(depend_dir) && \
	tar xf $(openssl).tar.gz && \
	cd $(openssl) && \
	./config --prefix=$(openssl_home) && \
	sed -i 's/^CFLAG= /CFLAG= -fPIC /' Makefile && \
	make clean && \
	make && \
	make install
	@echo "================Install Openssl Finished================"

install-python:
	cd $(depend_dir) && \
	tar xf $(py).tar.bz2 && \
	cd $(py) && \
	sed -i \
	-e "s|include_dirs = ssl_incs|include_dirs = ['$(openssl_home)/include']|" \
	-e "s|library_dirs = ssl_libs|library_dirs = ['$(openssl_home)/lib']|" setup.py #&& \
	./configure --prefix=$(py_home) && \
	make clean && \
	make && \
	make install && \
	cp -r $(openssl_home)/include/openssl $(py_home)/include/python2.7/
	@echo "================Install Python Finished================"

install-pyOpenssl:
	cd $(depend_dir) && \
	tar xf $(pyssl).tar.gz && \
	cd $(pyssl) && \
	sed -i -e \
	"s|^IncludeDirs =.*|IncludeDirs = ['$(openssl_home)/include']|" \
	-e "s|^LibraryDirs =.*|LibraryDirs = ['$(openssl_home)/lib']|" \
	setup.py && \
	$(py_home)/bin/python setup.py clean && \
	$(py_home)/bin/python setup.py build && \
	$(py_home)/bin/python setup.py install
	@echo "================Install pyOpenssl Finished================"
	
install-func:
	cd $(cur_dir) && cd certmaster-0.28-uc && $(py_home)/bin/python setup.py install
	cd $(cur_dir) && cd func-0.28-uc && $(py_home)/bin/python setup.py install
	@echo "================Install Func Finished================"

install: install-openssl install-python install-pyOpenssl install-func
	@echo "================Fulll Installation Finished================"
