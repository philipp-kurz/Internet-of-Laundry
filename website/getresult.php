<?php
$mysqli = new mysqli("localhost", "phpmyadmin1", "internetoflaundry", "mqtt_data");
if($mysqli->connect_error) {
  exit('Could not connect');
}

$sql = "SELECT timestamp, milliamps FROM prototype ORDER BY timestamp DESC LIMIT 1";

$stmt = $mysqli->prepare($sql);
$stmt->execute();
$stmt->store_result();
$stmt->bind_result($timestamp, $milliamps);
$stmt->fetch();
$stmt->close();

echo $timestamp;
echo " ";
echo $milliamps;
?>