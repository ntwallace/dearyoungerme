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

	$result=mysql_query("SELECT * FROM `twilio_input` ORDER BY `timestamp` ASC", $link);

	echo '<table><tr class="header"><th>&nbsp;ID&nbsp;</th><th>&nbsp;Phone #&nbsp;</th><th>&nbsp;Message&nbsp;</th><th>&nbsp;Zip Code&nbsp;</th><th>&nbsp;Score&nbsp;</th><th>&nbsp;Timestamp&nbsp;</th></tr>';

	if($result!==FALSE){
		     while($row = mysql_fetch_array($result)) {
		        printf("<tr class='data'><td> &nbsp;%s </td><td> &nbsp;%s&nbsp; </td><td> &nbsp;%s&nbsp; </td><td> &nbsp;%s&nbsp; </td><td> &nbsp;%s&nbsp; </td><td> &nbsp;%s&nbsp; </td></tr>", 
		           $row["id"], $row["phone_number"], $row["message"], $row["zipcode"], $row["score"], $row["timestamp"]);
		     }
		     mysql_free_result($result);
		     mysql_close();
		  }

	echo '</table>';

	mysql_free_result($result);
	mysql_close();
?>
