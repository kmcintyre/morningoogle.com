cd ../python
python index.py
cd ../bin
python ~/6998159/s3copy.py -b morningoogle.com -f index.html -t index.html -c 'text/html' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/javascripts/mg.js -t javascripts/mg.js -c 'text/javascript' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/stylesheets/css-reset.min.css -t stylesheets/css-reset.min.css -c 'text/css' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/stylesheets/style.css -t stylesheets/style.css -c 'text/css' -p public-read -e gzip
python ~/6998159/s3copy.py -b morningoogle.com -f ~/morningoogle.com/public/favicon.ico -t favicon.ico -c 'image/x-icon' -p public-read
