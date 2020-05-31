<?php
$servername = "localhost";
$username = <MySQL_User>;
$password = <MySQL_Password>;
$dbname = "mqtt_data";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$machine = $_POST["machine"];

$sql = "UPDATE email_notifications SET sent = 1 WHERE sent = 0 AND machine = ".$machine;
echo $sql;
if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
