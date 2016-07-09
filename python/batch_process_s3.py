import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('morningoogle.com')
s3_client=boto3.client('s3')
print bucket
import video
import os

'''
for obj in bucket.objects.filter(Prefix='ogv'):
    if obj.key.endswith('.ogv'):
        video_file = obj.key.split('/')[-1]
        video_prefix = video_file.split('.')[0]
        video_mp4 = video_prefix + '.mp4' 
        video_gif = video_prefix + '.gif' 
        if len(list(bucket.objects.filter(Prefix='preview/' + video_gif))) == 0:
            print video_file
            s3_client.download_file('morningoogle.com', obj.key, video_file)
            encode_result = video.launch_avi_mp4(video_file, video_mp4)
            print 'encode video result:', encode_result
            
            os.remove(video_file)
             
            data = open(video_mp4, 'rb')
            s3.Bucket('morningoogle.com').put_object(Key='video/' + video_mp4, Body=data, ACL='public-read', ContentType='video/mp4')
                    
            png_result = video.launch_mp4_preview(video_mp4)
            print 'png result:', png_result
            
            os.remove(video_mp4)
    
            gif_result = video.launch_preview_gif(video_gif)
            print 'gif result:', gif_result
            
            filelist = [ f for f in os.listdir('.') if f.endswith('.png') ]
            for f in filelist:
                os.remove(f)
            
            data2 = open(video_gif, 'rb')
            s3.Bucket('morningoogle.com').put_object(Key='preview/' + video_gif, Body=data2, ACL='public-read', ContentType='image/gif')
            
            os.remove(video_gif)
'''

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