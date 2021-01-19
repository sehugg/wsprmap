all:
	gzip -cd data/wsprspots-2020-12.csv.gz | time python genmaps.py
	pngquant -f --nofs --ext .png output/*.png
	