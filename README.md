morningoogle.com
================

[morningoogle.com](http://morningoogle.com "MorninGoogle") - a mash-up of google search and audio

This project is non-commercial used as a means to review Amazon Elastic Transcoder and AWS Lambda, and test out Boto3 which seems to be significantly different than Boto.

Back-end
-------------

[python twisted](https://twistedmatrix.com), [Qt5](http://doc.qt.io/qt-5), [OpenCV](http://opencv.org), [Boto3](http://github.com/boto/boto3) and [ImageMagick](http://www.imagemagick.org)

My review of [Amazon Elastic Transcoder](https://aws.amazon.com/elastictranscoder) and [AWS Lambda](https://aws.amazon.com/lambda) is that Lambda needs GPU.  

Front-end
-------------

The front-end is server-side rendered [Jade](http://jade-lang.com) and [Express](http://expressjs.com) published via [s3copy.py](https://gist.github.com/kmcintyre/6998159) to [Amazon S3](http://aws.amazon.com/s3/)

[![Morning Google from 2014-05-20](http://img.youtube.com/vi/BeutJydMRKE/0.jpg)](http://www.youtube.com/watch?v=BeutJydMRKE)