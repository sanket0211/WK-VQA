<!DOCTYPE HTML>
<html>
<body>
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

<table style="width:100%">
<tr>
  <th>Image Id</th>
  <th>Image</th>
  <th>wikiCap</th>
  <th>Potential People-I</th>
  <th>Potential People-II</th>
  <th> Questions </th>
  <th>Help images</th>
</tr>

<?php
$count=0;
$st=$_GET["ST"];
$en=$_GET["EN"];
?>
<form action = './act3.php' method = 'post'>
<?php
$fileHandle = fopen("/home/sanket/kvqa/phase1AnnCloseList.csv", "r");
$ann_left = fopen("ann3_left/re_annotation.csv", "r");
$left_img_ids = array();
array_push($left_img_ids,-1);
$c=1;
while (($row = fgetcsv($ann_left, 0, "\t")) !== FALSE) {
	if($row==""){
		break;
	}
	if($c<$st){
		$c=$c+1;
		continue;
	}
	if($c>=$st and $c<=$en){
		array_push($left_img_ids,$row[0]);
	}
	$c=$c+1;
	if($c>$en){
		break;
	}
}
$count=0;
while (($row = fgetcsv($fileHandle, 0, "\t")) !== FALSE) {
      $count=$count+1;
	  /*if ($count>3){
		break;
	  }*/

	  if(array_search($count,$left_img_ids)==FALSE){
		continue;
	  }	  

?>


<tr>
    <td>
    <?php echo $count; ?>
    </td>
    
    <td>
     <img src="<?php echo "../".$row[0]; ?>" alt="Random image" ,width=180px, height=180px /><br>
    </td>
    
    <td>
    <?php echo $row[3]; ?>
    </td>

    <td>
    <?php echo $row[7]; ?>
    </td>

    <td>
    <?php echo $row[8]; ?>
    </td>

   
    <td>
    <input type="text" name="Q1<?php echo $count; ?>" > Who is in left?<br><br>
    <input type="text" name="Q2<?php echo $count; ?>"> Who is in center?<br><br>
    <input type="text" name="Q3<?php echo $count; ?>"> Who is in right?<br><br>
    <input type="radio" name="Q4<?php echo $count; ?>" value="NOT SURE">I am not sure<br><br>
    <input type="radio" name="Q5<?php echo $count; ?>" value="ONE">One face<br><br>
    <input type="radio" name="Q6<?php echo $count; ?>" value="TWO">two face<br><br>
    <input type="radio" name="Q7<?php echo $count; ?>" value="FOUR">four face<br><br>
    <input type="radio" name="Q8<?php echo $count; ?>" value="FIVE">five face<br><br>
    <input type="radio" name="Q9<?php echo $count; ?>" value="MORE">more face<br><br>
    <input type="radio" name="Q10<?php echo $count; ?>" value="NO">no face<br><br>

    </td>

    <td>
    <?php echo $row[2]; ?>
    <br>
    <?php echo "<a href=https://en.wikipedia.org/wiki/".$row[2]." target=_blank>Wiki Link</a>"; ?>
    <br>
       <img src="<?php echo "../wikiDP/".$row[2]."/1.jpg"; ?>" alt="Random image" ,width=180px, height=180px /><br>
    <br>
    <?php echo "<a href=https://www.google.co.in/search?q=".$row[2]."&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjd0e728azaAhVMr48KHZEFAaUQ_AUICigB&biw=1855&bih=982 target=_blank>Google Link</a>"; ?>
    </td>

</tr>
<?php
}
?>
</table>

<input type="text" name="stInd" value=<?php echo $st; ?>>start id
<input type="text" name="enInd" value=<?php echo $en; ?>>end Id<br><br>

<input type = 'submit' value = 'Save and Go To Next'>
<?php echo $_POST["stInd"]; ?>
<?php echo $_POST["enInd"]; ?>
</form>


</body>
</html>


