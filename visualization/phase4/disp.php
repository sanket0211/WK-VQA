<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;
}
</style>
</head>
<body>

<table style="width:100%">
<tr>
  <th>Image Id</th>
  <th>Image</th>
  <th>Wiki category</th>
  <th>Wiki Name</th>
  <th>WikiCap </th>
  <th>msCap</th>
  <th>#faces detected (MTCNN)</th>
</tr>
<?php
$st=$argv[1];;
$en= $argv[2];
$count=0;
//Open the file.
$fileHandle = fopen("faceDetCleaned0.0.csv", "r");
while (($row = fgetcsv($fileHandle, 0, "\t")) !== FALSE) {
      $count=$count+1;
      if($count<$st)
        continue;
      if($count>$en)
        break;

      echo "<tr><td>";
      echo $count;
      echo "</td><td>";
      echo '<img src="' . $row[0] . '" alt="Random image" ,width=80px, height=80px /><br>';
      echo "</td><td>";
      echo $row[1];
      echo "</td><td>";
      echo $row[2];
      echo "</td><td>";
      echo $row[3];
      echo "</td><td>";
      echo $row[4];
      echo "</td><td>";
      echo $row[5];
      echo "</td></tr>";
      echo "\n";
}
?>
</table>
