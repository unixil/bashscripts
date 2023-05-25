#! /usr/bin/perl

package get_color_scheme;

use warnings;
use strict;
use Switch;
use String::Util qw(trim);


sub extract_files {
    my ($path) = @_;
    my @arr ;
    if ( opendir( DIR, $path )  || die "can't open $path\n" ){
        @arr = grep { -f "$path/$_" } readdir(DIR);
        @arr = sort @arr;
        @arr = map  { "$path/$_"; } @arr;
    }
    @arr;
}



sub extract_color_scheme{
    my $filename;
    ($filename) = @_;
    my $fh;
    open($fh, '<', $filename) or die " could not open file '$fh', $!";
    my $row;
    
    my $scheme_color;
    my %scheme_table;
    
    
    while($row = <$fh>){
        if(length($row //= "")){
            my @words = split "  ", $row;
            if (scalar @words >1 ){
    	        $scheme_table{"$words[0]"} = trim($words[-1]);
    	    }
        }
    }
    my $k;
    my $v;
    my $num;
    $scheme_color="";
    my $color_tmp;
    while (($k, $v) = each %scheme_table){
        my $a;
        ($a) = trim($v);
        if($k =~ /color/){
	    ($num) = $k=~/([0-9]+)/;
	    $scheme_color = ${scheme_color}."\033]"."4;${num};$a"."\007";	    
	}
        elsif($k =~ /foreground/){
    	    $scheme_color = "\033]"."10;$a"."\007".$scheme_color;
        }elsif($k =~ /background/){
    	    $scheme_color = "\033]"."11;$a"."\007".$scheme_color;	    
        }elsif($k =~ /Color/){
    	    $scheme_color = "\033]"."12;$a"."\007".$scheme_color;	    
        }
    }
    my @scheme_info_list=();
    $scheme_info_list[0]=$filename;
    $scheme_info_list[1]=$scheme_color;

    close($fh);
    @scheme_info_list;
    
}

sub get_all_color_schemes{
    my ($color_scheme_dir) = @_;
    my @color_scheme_files;
    (@color_scheme_files) = extract_files($color_scheme_dir);
    my $color_scheme_file;
    my %color_schemes_dict;
    my @color_scheme_info_list;

    my $theme_name;
    foreach $color_scheme_file (@color_scheme_files){
        (@color_scheme_info_list) = extract_color_scheme($color_scheme_file);
	$theme_name = $color_scheme_info_list[0] =~ s/$color_scheme_dir//r;
	$theme_name=substr($theme_name,1,-4); # cut the beginning / and the .txt ending of file name
	$color_schemes_dict{$theme_name} = $color_scheme_info_list[1];
    }
    %color_schemes_dict;
}

get_all_color_schemes("/home/lixin/.themes/urxvt");

1;





=pod	
# gabages I tried :(


#	    my $a;
#	    ($a) = trim($v);
#	    print $a;

#	    $scheme_color = ${scheme_color} . '\\033]4;' .  ${num} . ';' . $a . '\\007';
	    #	    $scheme_color = ${scheme_color} . '\033]4;' .  ${num} . ';' . ${a} . '\007';
#	    $scheme_color = join("",qq(${scheme_color}) , "\\033]4;" , qq(${num}) , ";" , qq(${a}) , "\\","007");



	    #    	    $scheme_color = '\033]11;' . trim($v) . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\033]11;' . $a . '\007' . ${scheme_color};
#    	    $scheme_color = '\033]11;' . $a . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\033]11;' . $a . '\007' . ${scheme_color};
#    	    $scheme_color = join("" , "\\033]11;" . $a , "\\","007" , ${scheme_color});


	    #            $scheme_color = '\033]10;' . $v =~ s/[\n]+$// . '\007' . trim($v);
#    	    $scheme_color = '\033]10;' . trim($v) . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\033]10;' . $a . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\033]10;' . $a . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\\033]10;' . $a . '\\007' . ${scheme_color};
#   	    $scheme_color = join("" , "\\033]10;" . $a , "\\","007" , ${scheme_color});	    	    


	    #            $scheme_color = '\033]12;' . $v =~ s/[\n]+$// . '\007' . trim($v);
#    	    $scheme_color = '\033]12;' . trim($v) . '\007' . ${scheme_color};
#    	    $scheme_color = '\033]12;' . $a . '\007' . ${scheme_color};
	    #    	    $scheme_color = '\033]12;' . $a . '\007' . ${scheme_color};
#    	    $scheme_color = join("" , "\\033]12;" . $a , "\\","007" , ${scheme_color});	    	    	    



#    print "hi\n";
#    print $scheme_color;


    my $k;
    my $v;
    while( ($k,$v) = each %color_schemes_dict){

	$theme_name=$k;

	if(defined($color_scheme_dir)){
	    $theme_name =~ s/$color_scheme_dir//gr;
	    print $theme_name;
	}

	print $k;
        print "\n\n";
        print $v;
        print "\n\n\n\n";
    }
=cut
