<html>
<head>
<link rel="icon" type="image/vnd.microsoft.icon" href="stacks.ico" />
<title> Location of tag </title>
</head>
<body>

<p align=left>
<a href="index.html">stacks project</a> | <a href="query.php">search</a> | <a href="tags.html">tags explained</a>
</p>

<?php
$TAG=strtoupper($_GET["tag"]);
echo "<div style=\"margin-left: auto; margin-right: auto; text-align: left; width: 600px\">\n";
if ((strlen($TAG) <> 4) or (ctype_alnum($TAG) == FALSE)) {
	echo "Malformed input!<br>\n";
	echo "Tags are 4 character strings of ";
	echo "digits and letters.<br>\n";
} elseif (file_exists("code/$TAG")) {
	include("code/$TAG");
} else {
	echo "Tag $TAG does not exist.<br>\n";
	echo "This may be because you mistyped it.<br>\n";
}
echo "For more on tags click ";
echo "<a href=\"tags.html\">here</a>. ";
echo "To try again click ";
echo "<a href=\"query.php\">here</a>.\n";
echo "</div>";
?>

</body>
</html>
