for i in markdown/*.markdown; do
	filename="${i#markdown/}";
	html="${filename%.markdown}.html";
	[ "$i" -nt "$html" ] && echo $i && pandoc -c stylesheets/main.css -s --latexmathml=mathml.js -o "$html" "$i";
done