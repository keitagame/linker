#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

my $q = CGI->new;

# フォームが未送信ならフォームを表示
if (!$q->param('submit')) {
    print "Content-Type: text/html\n\n";
    print <<'HTML';
<h1>相互リンク登録フォーム</h1>
<form action="register.cgi" method="post" enctype="multipart/form-data">
  key: <input type="text" name="key"><br>
  あなたのURL: <input type="text" name="url"><br>
  <input type="submit" name="submit" value="登録">
</form>
HTML
    exit;
}

# フォーム送信後の処理
print "Content-Type: text/html\n\n";

my $key = $q->param('key') || '';
my $url = $q->param('url') || '';


if (!$key || !$url) {
    print "key, url, バナー画像を入力してください。";
    exit;
}



# links.txt に保存
open my $fh, ">>", "data/links.txt" or die "書き込み不可: $!";
print $fh "$key|$url\n";
close $fh;
if (-e "data/links.txt") {
    open my $pfh, "<", "data/links.txt" or die "読み込み不可: $!";
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
# A側が貼るべき仮バナー
my $my_banner = "http://keitagames.com/links/banner.cgi?key=$key";
my $my_link = "http://keitagames.com/links/link.cgi?key=$key";

print "<h3>登録完了</h3>";
print "Please place the banner and link on your website.：<br>";
print qq(<img src="$my_banner"><br><br>);

print qq(<code>バナー:$my_banner</code><br>);
print qq(<code>リンク:$my_link</code>);
