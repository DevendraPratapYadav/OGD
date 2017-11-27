<?php

if(isset($_POST['name']) && isset($_POST['email'])) {	//get the parameter from js
	getPageData($_POST['name'], $_POST['email']);
}

	
function connectToDB() {
	$mysqliLink = new mysqli('localhost', 'root', '', 'ogd'); //ogd is name of database
	
	if(mysqli_connect_errno()) {
		exit();
	}
	
	return $mysqliLink;
}

function getPageData($name, $email) {
	$mysqliLink = connectToDB();
	
	$query = $mysqliLink->query("SELECT * FROM Users WHERE ID = '$email'"); //Users is name of table
	
	//just making variables to collect all columns of database
	$db_serial = NULL;
	$db_name = NULL;
	$db_id = NULL;
	$db_timeLog = NULL; 

	if(mysqli_num_rows($query) != 0) { // entry exists
		if($row = $query->fetch_object()) {
			$db_serial = $row->Entry;
			$db_name = $row->Name;
			$db_id = $row->ID;
			$db_timeLog = $row->Log;
		}
		$db_timeLog++;
		// echo $db_timeLog;
		
		$updateQuery = $mysqliLink->query("UPDATE Users SET timeLog = '$db_timeLog' WHERE id = '$email'");
	}
	else { // make new entry
		$insertQuery = $mysqliLink->query("INSERT INTO Users (name, id, log) VALUES ('$name', '$email', 1)");
		// echo "new entry created";
	}
}

?>
