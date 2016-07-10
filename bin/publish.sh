wget http://localhost:3000 -O index.html

python ~/6998159/s3copy.py -b morningoogle.com -f index.html -t index.html -c 'text/html' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/images/morningoogle.png -t images/morningoogle.png -c 'image/png' -p public-read
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/javascripts/mg.js -t javascripts/mg.js -c 'text/javascript' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/stylesheets/css-reset.min.css -t stylesheets/css-reset.min.css -c 'text/css' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/stylesheets/style.css -t stylesheets/style.css -c 'text/css' -p public-read -e gzip

rm index.html
