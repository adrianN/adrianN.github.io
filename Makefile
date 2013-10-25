PANDOC_OPT = -c stylesheets/main.css -s

index.html : index.markdown
	pandoc $(PANDOC_OPT) -o index.html index.markdown