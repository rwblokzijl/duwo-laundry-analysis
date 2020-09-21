all: clean prepare run package

clean:
	rm data
	rm -r plots
	rm laundry_plots.zip
	pipenv --rm

prepare:
	mkdir plots
	scp git.blokzijl.family:both ./data
	jupyter nbconvert --to script main.ipynb
	pipenv install

run:
	pipenv run python main.py

package:
	cp data plots/data.txt
	zip -r laundry_plots.zip plots

