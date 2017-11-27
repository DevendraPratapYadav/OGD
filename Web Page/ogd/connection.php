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
	echo "Connected successfully";

    $sql = "SELECT * FROM ogd.mortality";
	$result = mysqli_query($conn, $sql);

	if (mysqli_num_rows($result) > 0) {
		// output data of each row
		echo "<br>";
		while($row = mysqli_fetch_assoc($result)) {
		    echo "State: " . $row["state"]. " - Year: " . $row["year"]. " Rate: " . $row["rate"] . "<br>";
		}
	}	
	else {
		echo "0 results";
	}

	mysqli_close($conn);
?> 