#!/usr/bin/perl
use strict;
use Data::Dumper;

my %loops;

while (<>) {
	my $line = $_;
	chomp($line);

	if ($line =~ /# Loop (\d+) \(([^)]+)\) : (.+) with (\d+) ops/) {
		$loops{$1} = [$1, $2, $3, $4, 0];
	}

	if ($line =~ /entry (\d+):(\d+)/) {
		if ($loops{$1}) {
			$loops{$1}[4] = $2;
		}
	}
}

my $total_ops = 0;
foreach my $loop (values %loops) {
	$total_ops += $loop->[4] * $loop->[3];
}

foreach my $k (sort { $a <=> $b } keys %loops) {
	my $loop = $loops{$k};
	print sprintf("Loop #%d (%s) type=%s ops=%d called=%d total=%d (%0.2f\%)\n",
		$loop->[0], $loop->[1], $loop->[2], $loop->[3], $loop->[4], $loop->[3] * $loop->[4],
		$loop->[3] * $loop->[4] * 100.0 / $total_ops)
}

print "\ntotal_ops=$total_ops\n";