<?php
$servername = "localhost";
$username = "phpmyadmin1";
$password = "internetoflaundry";
$dbname = "mqtt_data";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$name = $_POST["name"];
$email = $_POST["email"];
$machine = $_POST["machine"];

$sql = "INSERT INTO email_notifications (address, name, machine)
VALUES ('".$email."','".$name."',".$machine.")";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>