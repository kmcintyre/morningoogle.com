import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('morningoogle.com')
print bucket
import os

for mp3 in os.listdir('../audio'):
    print mp3
    objs = list(bucket.objects.filter(Prefix='audio/' + mp3))
    if len(objs) > 0:
        print 'exists:', mp3
        print objs[0].key
        
        exit(0)
        #get().download_file('test.mp3')
    else:
        print 'missing:', mp3
        data = open('../audio/' + mp3, 'rb')        
        bucket.put_object(ACL='public-read', Key='audio/' + mp3, Body=data)        

'''
import transcoder
for obj in bucket.objects.filter(Prefix='ogv'):
    video_prefix = obj.key.split('/')[1].split('.')[0]
    if video_prefix:
        mp4 = 'video/' + video_prefix + '.mp4'
        objs = list(bucket.objects.filter(Prefix=mp4))
        if len(objs) > 0 and objs[0].key == mp4:
            print 'exists:', mp4
        else:
            print 'missing:', mp4
            response = transcoder.toMp4(obj.key, video_prefix)
            print 'response:', response
'''            