get:
	scp 192.168.0.25:laundry_stats ./data

install:
	pipenv install

prepare:
	mkdir plots

run:
	pipenv run python main.py

package:
	cp data plots/data.txt
	zip -r laundry_plots.zip plots

clean:
	rm data
	rm -r plots
	rm laundry_plots.zip

build:
	rm main.py
	jupyter nbconvert --to script main.ipynb

uninstall:
	pipenv --rm

all: clean prepare run package

full: install get build all uninstall

