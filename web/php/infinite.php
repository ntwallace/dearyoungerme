<?php

	function connection(){
		$server="localhost";
		$user="popup";
		$pass="windows";
		$db="popup";
	   	
		$connection = mysql_connect($server, $user, $pass);

		if (!$connection) {
	    	die('MySQL ERROR: ' . mysql_error());
		}
		
		mysql_select_db($db) or die( 'MySQL ERROR: '. mysql_error() );

		return $connection;
	}

	$link=connection();

	$whereType = mysql_real_escape_string($_POST['searchType']);
	$whereVal = mysql_real_escape_string($_POST['searchVal']);

	if(!$whereVal) {
		$result=mysql_query("SELECT * FROM `twilio_input` WHERE `phone_number` NOT IN ('+13478511138','+17134169394', '+12063903298', '+13019198751') GROUP BY `message` ORDER BY `id` DESC LIMIT 50", $link);
	} else {
		$result=mysql_query("SELECT * FROM `twilio_input` WHERE `phone_number` NOT IN ('+13478511138','+17134169394', '+12063903298', '+13019198751') AND $whereType LIKE '%$whereVal%' GROUP BY `message` ORDER BY `id` DESC", $link);
	}

	if($result!==FALSE){
		     while($row = mysql_fetch_array($result)) {
		        printf("<div class='data-row'><div class='message'>%s</div><div class='subheader'><div class='number'>%s</div><div class='time'>%s</div></div></div>", 
		           $row["message"], 'xxx-xxx-'.substr($row["phone_number"], -4), date('m/d h:m', strtotime($row["timestamp"])));
		     }
		     mysql_free_result($result);
		     mysql_close();
		  }
?>
