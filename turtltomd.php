#!/usr/bin/php
<?php

function sanitize_filename($s) {
	$s = preg_replace('/[_\/\|\"]/',' ',$s) ;
	$s = preg_replace('/\.+/','.',$s) ;
	return $s ;
}

if ( !isset($argv[1]) ) {
	die ("USAGE: {$argv[0]} turtl_backup_file.json") ;
}

$j = json_decode ( @file_get_contents($argv[1]) ) ;
if ( !isset($j) or $j === null ) {
	die ("File {$argv[1]} does not exist, or is not valid JSON") ;
}

@mkdir ( "output_md" ) ;
#@mkdir ( "output_md/no_board" ) ;


$spaces = [] ;
foreach ( $j->spaces AS $s ) {
	$spaces[$s->id] = sanitize_filename($s->title) ;
	@mkdir ("output_md/{$s->title}" ) ;
}

$boards = [];
foreach ( $j->boards AS $b ) {
	$space_name = $spaces[$b->space_id] ;
	$board_title = "{$space_name}/" . sanitize_filename($b->title) ;
	$boards[$b->id] = $board_title ;
	@mkdir ( "output_md/$board_title" ) ;
}

foreach ( $j->notes as $n ) {
	if ( !isset($n->board_id) or $n->board_id === null ) $board_title = $spaces[$n->space_id] ;
	else $board_title = $boards[$n->board_id] ;
	$add = '' ;
	do {
		$filename = "output_md/{$board_title}/" . sanitize_filename($n->title) ;
		if ($add == '' ) $add = 2 ;
		else {
			$filename .= "-{$add}" ;
			$add++ ;
		}
		$filename .= '.md' ;
		$continue = file_exists($filename) ;
	} while ($continue) ;
	# Support more note types here
	if ( isset($n->password) ) $text = $n->password ;
	else $text = $n->text ;
	file_put_contents ( $filename , $text ) ;
}

?>
