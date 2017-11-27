<?php

	$servername = "localhost";
	$username = "root";
	$password = "";

	// Create connection
	$conn = mysqli_connect($servername, $username, $password);

	// Check connection
	if (!$conn) {
	    die("Connection failed: " . mysqli_connect_error());
	}

    $sql = "SELECT * FROM ogd.imortality";
	$result = mysqli_query($conn, $sql);


	if (mysqli_num_rows($result) > 0) {

		$rows = array();
		while($r = mysqli_fetch_assoc($result)) {
		    $rows[] = $r;
		}

		echo json_encode($rows);
	}	
	else {
		echo "0 results";
	}

	mysqli_close($conn);
?>