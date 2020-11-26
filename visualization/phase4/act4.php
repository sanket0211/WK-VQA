<html>
<body>
<?php 
$st=$_POST["stInd"];
$en=$_POST["enInd"];
$annFile=sprintf("ann4_left/numFaceAnn-%u-%u.txt", $st, $en);
$file = fopen($annFile,"w+") or die("Can't open file");
$ann_left = fopen("ann4_left/re_annotation.csv", "r");
$left_img_ids = array();
$count=0;
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
	if($c>$en){
		break;
	}
	$c=$c+1;


}



//for ($i = $st; $i <= $en; $i++) {
for ($i = 0; $i < sizeof($left_img_ids); $i++) {

	fwrite($file, $left_img_ids[$i]);
	fwrite($file,"\t");
	$A1=$_POST['Q1' . $left_img_ids[$i]]."\t";
	$A2=$_POST['Q2' . $left_img_ids[$i]]."\t";
	$A3=$_POST['Q3' . $left_img_ids[$i]]."\t";
	$A4=$_POST['Q4' . $left_img_ids[$i]]."\t";
	$A5=$_POST['Q5' . $left_img_ids[$i]]."\t";
	$A6=$_POST['Q6' . $left_img_ids[$i]]."\t";
	$A7=$_POST['Q7' . $left_img_ids[$i]]."\t";
	$A8=$_POST['Q8' . $left_img_ids[$i]]."\t";
	$A9=$_POST['Q9' . $left_img_ids[$i]]."\t";
	$A10=$_POST['Q10' . $left_img_ids[$i]]."\t";
	$A11=$_POST['Q11' . $left_img_ids[$i]]."\n";
	$txt=$A1.$A2.$A3.$A4.$A5.$A6.$A7.$A8.$A9.$A10.$A11;
	fwrite($file, $txt);

}
fclose($file);

if(fmod($en,10)==0)
  echo "Thanks, please ask Rajan Sir for the next link";
  else
  {
  $st=$en+1;
  $en=$en+5;
#$url="http://dosa.cds.iisc.ac.in/VQA-disp/dispWikiVQA/phase3/ann4.php?ST=$st&EN=$en";
  $url="http://127.0.0.1/kvqa/phase4/ann4.php?ST=$st&EN=$en";
  header("Location: $url"); 
  exit();
  }
?>
</body>
</html> 
