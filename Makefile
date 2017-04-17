#!/usr/bin/env make -f

PYPY_DIR ?= pypy
RPYTHON  ?= $(PYPY_DIR)/rpython/bin/rpython


ifdef MATE
	TARGET  = src/mate_targetsomstandalone.py
	COMMAND = ./mate.sh

	ifdef JIT
		JIT_ARGS = -Ojit
		BIN  = ./RTruffleMATE-jit
	else
		BIN = ./RTruffleMATE-no-jit
	endif
else
	TARGET      = src/targetsomstandalone.py
	COMMAND = ./som.sh

	ifdef JIT
		JIT_ARGS = -Ojit
		BIN  = ./RTruffleSOM-jit
	else
		BIN = ./RTruffleSOM-no-jit
	endif
endif

all: compile

compile: core-lib/.git
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) $(RPYTHON) --batch $(JIT_ARGS) $(TARGET)

somtest: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate TestSuite/TestHarness.som

matetest: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite TestSuite/MateMOPSuite/MateTestHarness.som

test:
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) nosetests

vmtest:
	$(BIN) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate TestSuite/TestHarness.som;

som-micro:
	rebench -c benchmarks.conf som-micro vm:RTruffleSOM-no-jit

mate-micro:
	rebench -c benchmarks.conf mate-micro vm:RTruffleMATE-no-jit

clean:
	@rm -f RTruffleSOM-no-jit
	@rm -f RTruffleSOM-jit
	@rm -f RTruffleMATE-no-jit
	@rm -f RTruffleMATE-jit

core-lib/.git:
	git submodule update --init --recursive --remote
