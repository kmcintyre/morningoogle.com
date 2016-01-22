def toMp4(incoming, outgoing):    
    import boto3
    client = boto3.client('elastictranscoder')    
    response = client.create_job(
        PipelineId='1453398326915-jvsbts',
        Input={
            'Key': incoming
        },
        Output={
            'Key':  'video/' + outgoing + '.mp4',
            'ThumbnailPattern':  'thumb/' + outgoing + '-{count}',
            'PresetId': '1351620000001-100070'
        }
    )
    return response