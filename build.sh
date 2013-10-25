for i in *.markdown; do
	[ "$i" -nt "${i%.*}.html" ] && pandoc -c stylesheets/main.css -s -o "${i%.*}.html" "$i";
done