#!/usr/bin/env make -f

PYPY_DIR ?= pypy
RPYTHON  ?= $(PYPY_DIR)/rpython/bin/rpython
COMMAND   = ./som.sh
TARGET    = src/targetsomstandalone.py

ifdef JIT
	JIT_ARGS = -Ojit
	BIN = ./RTruffleSOM-jit
	VM = 'jit'
else
	BIN = ./RTruffleSOM-no-jit
	VM = 'no-jit'
endif

all: compile

compile: core-lib/.git
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) $(RPYTHON) --batch $(JIT_ARGS) $(TARGET)

som-test: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som

mate-test: core-lib/.git
	$(COMMAND) --mate -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite:TestSuite/Mate TestSuite/TestHarness.som

test:
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) nosetests

somvm-test:
	$(BIN) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som;

matevm-test:
	$(BIN) --mate -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite/Mate TestSuite/TestHarness.som;

matevmmatetestsuite:
	$(BIN) --mate -cp Smalltalk:Smalltalk/Mate:Smalltalk/Mate/MOP:TestSuite:TestSuite/MateMOPSuite:Examples/Benchmarks/Mate/Immutability:Examples/Benchmarks/Mate/Immutability/DelegationProxies::Examples/Benchmarks/Mate/Immutability/Handles MateTestHarness.som;

som-micro:
	rebench -c benchmarks.conf som-micro vm:SOM-interpreter

mate-micro:
	rebench -c benchmarks.conf mate-micro vm:MATE-interpreter

somvm-micro:
	rebench -c benchmarks.conf som-micro vm:SOM-$(VM)

matevm-micro:
	rebench -c benchmarks.conf mate-micro vm:MATE-$(VM)

som-macro:
	rebench -c benchmarks.conf som-macro vm:SOM-interpreter

mate-macro:
	rebench -c benchmarks.conf mate-macro vm:MATE-interpreter

somvm-macro:
	rebench -c benchmarks.conf som-macro vm:SOM-$(VM)

matevm-macro:
	rebench -c benchmarks.conf mate-macro vm:MATE-$(VM)

#make BENCH=Storage.som som-bench
som-bench:
	./som.sh -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures:Examples/Benchmarks/Richards:Examples/Benchmarks/DeltaBlue:Examples/Benchmarks/NBody:Examples/Benchmarks/CD Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som somvm-bench
somvm-bench:
	$(BIN) -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures:Examples/Benchmarks/Richards:Examples/Benchmarks/DeltaBlue:Examples/Benchmarks/NBody:Examples/Benchmarks/CD Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som mate-bench
mate-bench:
	./som.sh --mate -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures:Examples/Benchmarks/Richards:Examples/Benchmarks/DeltaBlue:Examples/Benchmarks/NBody:Examples/Benchmarks/CD Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som matevm-bench
matevm-bench:
	$(BIN) --mate -cp Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP:Examples/Benchmarks/LanguageFeatures:Examples/Benchmarks/Richards:Examples/Benchmarks/DeltaBlue:Examples/Benchmarks/NBody:Examples/Benchmarks/CD Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

clean:
	@rm -f RTruffleMATE-no-jit
	@rm -f RTruffleMATE-jit

core-lib/.git:
	git submodule update --init --recursive --remote
