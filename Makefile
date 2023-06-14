basic:
	python web_crawler.py -u $(URL) -t $(THRESHOLD) -o $(OUTPUT)
advanced:
	python customized_web_crawler.py -u $(URL) -t $(THRESHOLD) -o $(OUTPUT)
clean:
	rm -f ouput.txt Count_of_files_level.pdf Type_of_Files.pdf
