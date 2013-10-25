for i in *.markdown; do
	[ "$i" -nt "${i%.*}.html" ] && echo $i && pandoc -c stylesheets/main.css -s --latexmathml=mathml.js -o "${i%.*}.html" "$i";
done