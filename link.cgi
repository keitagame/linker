#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

my $q   = CGI->new;
my $key = $q->param('key') || '';

# key がない場合
if (!$key) {
    print "Content-Type: text/html\n\n";
    print "key が指定されていません。";
    exit;
}

# pairs.txt から相手のURLを探す
my $target_url;

if (-e "data/pairs.txt") {
    open my $pfh, "<", "data/pairs.txt" or die "読み込み不可: $!";
    while (my $line = <$pfh>) {
        chomp $line;
        my ($k, $url, $banner) = split /\|/, $line;
        if ($k eq $key) {
            $target_url = $url;
            last;
        }
    }
    close $pfh;
}

# 見つかったらリダイレクト
if ($target_url) {
    print "Status: 302 Found\n";
    print "Location: $target_url\n\n";
    exit;
}

# 見つからなかった場合（まだ相互リンク未成立）
print "Content-Type: text/html\n\n";
print "この key ではまだ相互リンクが成立していません。";
