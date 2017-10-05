#!/usr/bin/env make -f

PYPY_DIR ?= pypy
RPYTHON  ?= $(PYPY_DIR)/rpython/bin/rpython
COMMAND   = ./som.sh
TARGET    = src/targetsomstandalone.py

# BENCHS_INCLUDES = $(shell find Examples/Benchmarks -type d -printf '%p:')
BENCHS_INCLUDES = Examples/Benchmarks/Mate/IndividualOperations
FILESYSTEM_INCLUDES = Smalltalk/Collections/Streams:Smalltalk/FileSystem/Core:Smalltalk/FileSystem/Disk:Smalltalk/FileSystem/Streams
BASE_INCLUDES = Smalltalk:Smalltalk/Mate/:Smalltalk/Mate/MOP

ifdef JIT
	JIT_ARGS = -Ojit
	BIN = ./RTruffleMate-jit
	VM = jit
else
	BIN = ./RTruffleMate-no-jit
	VM = no-jit
endif

all: compile

compile: core-lib/.git
	PYTHONPATH=$(PYTHONPATH):$(PYPY_DIR) $(RPYTHON) --batch $(JIT_ARGS) $(TARGET)

som-test: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:TestSuite:TestSuite/Mate TestSuite/TestHarness.som

som-file-test: core-lib/.git
	$(COMMAND) -cp Smalltalk:Smalltalk/Mate/MOP:Smalltalk/Mate:Smalltalk/Collections/Streams:Smalltalk/FileSystem/Core:Smalltalk/FileSystem/Disk:Smalltalk/FileSystem/Streams:TestSuite/FileSystem:TestSuite TestSuite/FileSystem/FilesTestHarness.som


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
	./som.sh -cp $(BASE_INCLUDES):$(FILESYSTEM_INCLUDES):$(BENCHS_INCLUDES) Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som somvm-bench
somvm-bench:
	$(BIN) -cp $(BASE_INCLUDES):$(FILESYSTEM_INCLUDES):$(BENCHS_INCLUDES) Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som mate-bench
mate-bench:
	./som.sh --mate -cp $(BASE_INCLUDES):$(FILESYSTEM_INCLUDES):$(BENCHS_INCLUDES) Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

#make BENCH=Storage.som matevm-bench
matevm-bench:
	$(BIN) --mate -cp $(BASE_INCLUDES):$(FILESYSTEM_INCLUDES):$(BENCHS_INCLUDES) Examples/Benchmarks/BenchmarkHarness.som $(BENCH) 1 2 1

mate-iop:
	make BENCH=VMReflectiveArgumentRead.som mate-bench
	make BENCH=VMReflectiveFieldRead.som mate-bench
	# make BENCH=VMReflectiveFieldReadWithMetavariability.som mate-bench
	make BENCH=VMReflectiveFieldWrite.som mate-bench
	make BENCH=VMReflectiveLayoutFieldRead.som mate-bench
	make BENCH=VMReflectiveLayoutFieldWrite.som mate-bench
	make BENCH=VMReflectiveLocalVariableRead.som mate-bench
	make BENCH=VMReflectiveLocalVariableWrite.som mate-bench
	make BENCH=VMReflectiveMessageSend.som mate-bench
	make BENCH=VMReflectiveMethodActivation.som mate-bench
	make BENCH=VMReflectiveReturn.som mate-bench
	make BENCH=VMReflectiveSeveralObjectsFieldRead2.som mate-bench
	make BENCH=VMReflectiveSeveralObjectsFieldReadOneMO2.som mate-bench
	make BENCH=VMReflectiveSeveralObjectsFieldReadOneMO.som mate-bench
	make BENCH=VMReflectiveSeveralObjectsFieldRead.som mate-bench

matevm-iop:
	make BENCH=VMReflectiveArgumentRead.som matevm-bench
	make BENCH=VMReflectiveFieldRead.som matevm-bench
	# make BENCH=VMReflectiveFieldReadWithMetavariability.som matevm-bench
	make BENCH=VMReflectiveFieldWrite.som matevm-bench
	make BENCH=VMReflectiveLayoutFieldRead.som matevm-bench
	make BENCH=VMReflectiveLayoutFieldWrite.som matevm-bench
	make BENCH=VMReflectiveLocalVariableRead.som matevm-bench
	make BENCH=VMReflectiveLocalVariableWrite.som matevm-bench
	make BENCH=VMReflectiveMessageSend.som matevm-bench
	make BENCH=VMReflectiveMethodActivation.som matevm-bench
	make BENCH=VMReflectiveReturn.som matevm-bench
	make BENCH=VMReflectiveSeveralObjectsFieldRead2.som matevm-bench
	make BENCH=VMReflectiveSeveralObjectsFieldReadOneMO2.som matevm-bench
	make BENCH=VMReflectiveSeveralObjectsFieldReadOneMO.som matevm-bench
	make BENCH=VMReflectiveSeveralObjectsFieldRead.som matevm-bench

mate-aiop:
	make BENCH=VMReflectiveAllOperations.som mate-bench

matevm-aiop:
	make BENCH=VMReflectiveAllOperations.som matevm-bench

clean:
	@rm -f RTruffleMate-no-jit
	@rm -f RTruffleMate-jit

core-lib/.git:
	git submodule update --init --recursive --remote
