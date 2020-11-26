

<?php
function set_i($val){
	$one = $val + 2;
	$sec = $val - 2;
	echo "<div class='row'>";
	echo "  <div class='column' style='background-color:#aaa;'>";
	echo "<a href='entity_images.php?c=".$sec."'><button>Go to Previous Image</button></a>";
	echo "	</div>";
	echo "  <div class='column' style='background-color:#bbb;'>";
	echo "<a href='entity_images.php?c=".$one."'><button>Go to Next Image</button></a>";
	echo "	</div>";
	echo "	</div>";

}


function hello($x){	
	
	$dir    = '/home/sanket/kvqa/data/entity_images';
	$files1 = scandir($dir);
	$files2 = scandir($dir, 1);

	echo "<!DOCTYPE html>";
	echo "<html>";
	echo "<head>";
	echo "<meta name='viewport' content='width=device-width, initial-scale=1'>";
	echo "<style>";
	echo "* {";
	echo "    box-sizing: border-box;";
	echo "}";

	echo ".row {";
	echo "    display: flex;";
	echo "}";

	/* Create two equal columns that sits next to each other */
	echo ".column {";
	echo "    flex: 50%;";
	echo "    padding: 10px;";
	echo "}";
	echo "</style>";
	echo "</head>";
	echo "<body>";

	echo '<form action="entity_images.php" method="post">';
	echo "<div class='row'>";
	echo "  <div class='column' style='background-color:#aaa;'>";
	#echo 'Image Id: <input type="text" name="name" align="center"><br>';
	echo 'Image Id: <input list="name" name="name">';
	echo '<datalist id="name">';
	for($i=2;$i<sizeof($files1);$i++){
		//$id = preg_split("/[.jpg]/", $files1[$i]);
		$id = substr($files1[$i], 0, sizeof($files1[$i])-5);
		//$id = preg_split("/[-]/", $id[0]);
		echo '<option value="'.$id.'">';
	}

	echo '</datalist>';
	echo "</div>";
	echo "  <div class='column' style='background-color:#bbb;'>";
	echo '<input type="submit">';
	echo "</div>";
	echo "</div>";
	echo '</form>';

	set_i($x);

	echo "<div class='row'>";
	echo "  <div class='column' >";
	//$img_id = preg_split("/[.jpg]/", $files1[$x]);
	//$img_id = preg_split("/[-]/", $img_id[0]);
	$img_id = substr($files1[$x], 0, sizeof($files1[$x])-5);
	echo "    <h2>Image: ".$img_id."</h2>";
	//$myfile = fopen('/home/sanket/kvqa/phase1AnnCloseList.csv', "r");
	//$cnt=0;

	/*while($cnt<$img_id[0]){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		$url = $line[0];
		$cnt = $cnt + 1;
	}
	
	fclose($myfile);*/
	echo "<img src = 'entity_images/".$files1[$x]."' style = 'max-width:512px; max-height:512px;'></img>";
	/*$myfile = fopen('/home/sanket/kvqa/QAgeneratingFiles/QA_one/'.$files1[$x], "r");
	#echo "<img src = 'demo.jpeg'></img>";
	while(!feof($myfile)){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		echo "    <p>Q] ".$line[0]."</p>";
		echo "    <p><b>	".$line[1]."</b></p>";
	}
	fclose($myfile);*/
	
	echo "  </div>";
	echo "  <div class='column' >";
	$img_id = substr($files1[$x], 0, sizeof($files1[$x])-5);
	echo "    <h2>Image: ".$img_id."</h2>";
	/*$myfile = fopen('/home/sanket/kvqa/phase1AnnCloseList.csv', "r");
	$cnt=0;
	while($cnt<$img_id[0]){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		$url = $line[0];
		$cnt=$cnt+1;
	}
	fclose($myfile);*/
	echo "<img src = 'entity_images/".$files1[$x+1]."' style = 'max-width:512px; max-height:512px;'></img>";
	/*$myfile = fopen('/home/sanket/kvqa/QAgeneratingFiles/QA_one/'.$files1[$x+1], "r");
	while(!feof($myfile)){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		echo "    <p>Q] ".$line[0]."</p>";
		echo "    <p><b>".$line[1]."</b></p>";
	}
	fclose($myfile);*/
	echo "  </div>";
	echo "</div>";

	echo "</body>";
	echo "</html>";
/*
	while(!feof($myfile)) {
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		echo "<br>";
  		echo $line[0]."<br>";
  		echo $line[1] . "<br>";
	}

	$myfile = fopen('/home/sanket/wikiAttributesExtr/QA_one/'.$files1[$x+1], "r");
	echo "<img src = 'demo.jpeg'>";
	while(!feof($myfile)) {
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		echo "<br>";
  		echo $line[0] . "<br>";
	}
	fclose($myfile);*/
}

if (isset($_POST["name"])){
	$dir    = '/home/sanket/kvqa/data/entity_images';
	$files1 = scandir($dir);
	$file = $_POST["name"].".jpg";
	for($i=2;$i<sizeof($files1);$i++){
		if($files1[$i]==$file){
			hello($i);
			break;
		}
	}
	if($i>=sizeof($files1)){
		echo "File Not Found";
	}
}


if (isset($_GET['c'])) {
    hello($_GET['c']);
}


?>

