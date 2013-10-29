for i in markdown/*.markdown; do
	filename="${i#markdown/}";
	html="${filename%.markdown}.html";
	([ "$i" -nt "$html" ] || [ "template.txt" -nt "$html" ] || [ "include_after.txt" -nt "$html" ]) && 
	echo $i && 
	pandoc -c stylesheets/main.css -s -A include_after.txt --template=template.txt --latexmathml=mathml.js -o "$html" "$i";
done