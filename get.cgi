#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

my $q = CGI->new;

print "Content-Type: text/html\n\n";

my $key = $q->param('key') || '';
my $url = $q->param('url') || '';
my $upload = $q->upload('bannerfile');  # アップロードされたファイル

if (!$key || !$url || !$upload) {
    print "key, url, バナー画像を入力してください。";
    exit;
}
if (-e "data/pairs.txt") {
    open my $pfh, "<", "data/pairs.txt" or die "読み込み不可: $!";
    while (my $line = <$pfh>) {
        chomp $line;
        my ($k, $u, $b) = split /\|/, $line;
        if ($k eq $key) {
            print "<h3>この key はすでに相互リンク済みです</h3>";
            print "同じ key での再登録はできません。<br>";
            close $pfh;
            exit;
        }
    }
    close $pfh;
}
# ファイル名決定（例：keyベース）
my $filename = "img/$key.png";  # 拡張子は本当はMIME見て決めるのが理想

# 画像保存
open my $out, ">", $filename or die "保存できません: $!";
binmode $out;
while (my $chunk = <$upload>) {
    print $out $chunk;
}
close $out;

# A側の情報を探す（links.txt）
open my $fh, "<", "data/links.txt" or die "読み込み不可: $!";

my ($a_key, $a_url, $a_banner);
while (my $line = <$fh>) {
    chomp $line;
    my ($k, $u, $b) = split /\|/, $line;
    if ($k eq $key) {
        $a_key    = $k;
        $a_url    = $u;
        $a_banner = $b;
        last;
    }
}
close $fh;

if (!$a_key) {
    print "該当する key がありません。";
    exit;
}

# 相互リンク成立 → B側の情報を pairs.txt に保存
open my $pfh, ">>", "data/pairs.txt" or die "書き込み不可: $!";
print $pfh "$key|$url|$filename\n";
close $pfh;

print "<h3>相互リンク成立</h3>";

