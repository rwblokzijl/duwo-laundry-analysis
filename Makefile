all: clean prepare run package

get:
	rm data || true
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
	rm -r plots || true
	rm laundry_plots.zip || true

build:
	rm main.py || true
	jupyter nbconvert --to script main.ipynb

uninstall:
	pipenv --rm

full: install get build all uninstall

