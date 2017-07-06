#!/usr/bin/env make -f

PYPY_DIR ?= pypy
RPYTHON  ?= $(PYPY_DIR)/rpython/bin/rpython
COMMAND   = ./som.sh
TARGET    = src/targetsomstandalone.py

ifdef JIT
	JIT_ARGS = -Ojit
	BIN = ./RTruffleSOM-jit
else
	BIN = ./RTruffleSOM-no-jit
endif

all: compile

compile: core-lib/.git
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) $(RPYTHON) --batch $(JIT_ARGS) $(TARGET)

somtest: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som

matetest: core-lib/.git
	$(COMMAND) --mate -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite:TestSuite/Mate TestSuite/TestHarness.som

test:
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) nosetests

vmtest:
	$(BIN) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som;

matevmtest:
	$(BIN) --mate -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som;

som-micro:
	rebench -c benchmarks.conf som-micro vm:RTruffleSOM-no-jit

mate-micro:
	rebench -c benchmarks.conf mate-micro vm:RTruffleMATE-no-jit

#make BENCH=Storage.som som-bench
som-bench:
	./som.sh -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 0 1

#make BENCH=Storage.som mate-bench
mate-bench:
	./som.sh --mate -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 0 1

clean:
	@rm -f RTruffleMATE-no-jit
	@rm -f RTruffleMATE-jit

core-lib/.git:
	git submodule update --init --recursive --remote
