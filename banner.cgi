#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use GD;

my $q = CGI->new;
my $key = $q->param('key') || '';

print "Content-Type: image/png\n\n";

if (-e "data/pairs.txt") {
    open my $pfh, "<", "data/pairs.txt";
    while (my $line = <$pfh>) {
        chomp $line;
        my ($k, $url, $banner) = split /\|/, $line;
        if ($k eq $key && -e $banner) {
            open my $img, "<", $banner or last;
            binmode $img;
            print do { local $/; <$img> };
            close $img;
            exit;
        }
    }
    close $pfh;
}

my $im = GD::Image->new(200, 40);
my $white = $im->colorAllocate(255,255,255);
my $black = $im->colorAllocate(0,0,0);
$im->filledRectangle(0,0,300,50,$white);
$im->string(gdMediumBoldFont, 10, 15, $key, $black);
print $im->png;
