for i in markdown/*.markdown; do
	filename="${i#markdown/}";
	html="${filename%.markdown}.html";
	([ "$i" -nt "$html" ] || [ "build.sh" -nt "$html" ] || [ "template.txt" -nt "$html" ] || [ "stylesheets/main.css" -nt "$html" ] || [ "include_after.txt" -nt "$html" ]) && 
	echo $i && 
	pandoc -H stylesheets/main.css --smart -A include_after.txt --template=template.txt --latexmathml=mathml.js -o "$html" "$i";
done