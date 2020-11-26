

<?php
function set_i($val){
	$one = $val + 2;
	$sec = $val - 2;
	echo "<div class='row'>";
	echo "  <div class='column' style='background-color:#aaa;'>";
	echo "<a href='5.php?c=".$sec."'><button>Go to Previous Image</button></a>";
	echo "	</div>";
	echo "  <div class='column' style='background-color:#bbb;'>";
	echo "<a href='5.php?c=".$one."'><button>Go to Next Image</button></a>";
	echo "	</div>";
	echo "	</div>";

}


function hello($x){	

	$dir    = '/home/sanket/kvqa/QAgeneratingFiles/QA_five';
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

	echo '<form action="5.php" method="post">';
	echo "<div class='row'>";
	echo "  <div class='column' style='background-color:#aaa;'>";
#echo 'Image Id: <input type="text" name="name" align="center"><br>';
	echo 'Image Id: <input list="name" name="name">';
	echo '<datalist id="name">';
	for($i=2;$i<sizeof($files1);$i++){
		$id = preg_split("/[.]/", $files1[$i]);
		$id = preg_split("/[-]/", $id[0]);
		echo '<option value="'.$id[0].'">';
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
	$img_id = preg_split("/[.]/", $files1[$x]);
	$img_id = preg_split("/[-]/", $img_id[0]);
	echo "    <h2>Image: ".$img_id[0]."</h2>";
	$myfile = fopen('/home/sanket/kvqa/phase1AnnCloseList.csv', "r");
	$cnt=0;

	while($cnt<$img_id[0]){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		$url = $line[0];
		$cap = $line[3];
		$cnt = $cnt + 1;
	}

	fclose($myfile);
	$myfile = fopen('/home/sanket/kvqa/QAgeneratingFiles/QA_five/'.$files1[$x], "r");
	echo '<table border="1">';
	echo '<tr>';
	echo '<td>';
	echo "<img src = '".$url."' style = 'max-width:512px; max-height:512px;'></img>";
	echo '</td>';
	echo '</tr>';
	echo '<tr>';
	echo '<td align="center">'; 
	echo "<p>".$cap."</p>";
	echo '</td>';
	echo '</tr>';
	echo '</table>';
	$cnt=1;
#echo "<img src = 'demo.jpeg'></img>";
	while(!feof($myfile)){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		if($line[0]==""){
			break;
		}
		echo "    <p>Q".$cnt."] ".$line[0]."</p>";
		echo "    <p><b>	".$line[1]."</b></p>";
		$cnt=$cnt+1;
	}
	fclose($myfile);

	echo "  </div>";
	echo "  <div class='column' >";
	$img_id = preg_split("/[.]/", $files1[$x+1]);
	$img_id = preg_split("/[-]/", $img_id[0]);
	echo "    <h2>Image: ".$img_id[0]."</h2>";
	$myfile = fopen('/home/sanket/kvqa/phase1AnnCloseList.csv', "r");
	$cnt=0;
	while($cnt<$img_id[0]){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		$url = $line[0];
		$cap = $line[3];
		$cnt=$cnt+1;
	}
	fclose($myfile);
	$myfile = fopen('/home/sanket/kvqa/QAgeneratingFiles/QA_five/'.$files1[$x+1], "r");
	echo '<table border="1">';
	echo '<tr>';
	echo '<td>';
	echo "<img src = '".$url."' style = 'max-width:512px; max-height:512px;'></img>";
	echo '</td>';
	echo '</tr>';
	echo '<tr>';
	echo '<td align="center">'; 
	echo "<p>".$cap."</p>";
	echo '</td>';
	echo '</tr>';
	echo '</table>';
	$cnt=1;
	while(!feof($myfile)){
		$line = fgets($myfile);
		$line = preg_split("/[\t]/", $line);
		if($line[0]==""){
			break;
		}
		echo "    <p>Q".$cnt."] ".$line[0]."</p>";
		echo "    <p><b>".$line[1]."</b></p>";
		$cnt=$cnt+1;
	}
	fclose($myfile);
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

	   $myfile = fopen('/home/sanket/wikiAttributesExtr/QA_five/'.$files1[$x+1], "r");
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
	$dir    = '/home/sanket/kvqa/QAgeneratingFiles/QA_five';
	$files1 = scandir($dir);
	$file = $_POST["name"]."-QA.csv";
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

