# Create your views here.
from json import dumps

from boto import sts
from django.conf import settings
from django.http import JsonResponse


def get_s3_creds():
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    bucket = getattr(settings, 'S3_BUCKET_NAME', None)
    if not key or not secret or not bucket:
        return None
    else:
        return key, secret, bucket


# to be used for multipart upload
def get_sts_token(request):
    try:
        key, secret, bucket_name = get_s3_creds()

        policy_to_grant = {'Statement': [{'Action': ['s3:PutObject'],
                                          'Effect': 'Allow',
                                          'Resource': ['arn:aws:s3:::' + bucket_name + '/*']}]}
        sts_conn = sts.connect_to_region('us-east-1',  # edit and put the correct zone
                                         aws_access_key_id=key,
                                         aws_secret_access_key=secret)
        token = sts_conn.get_federation_token(name='iam_user',  # The name of the federated user
                                              duration=300,
                                              policy=dumps(policy_to_grant))
        return JsonResponse({'sts_token': token, 'status': 'ok'})
    except:
        return JsonResponse({'sts_token': None, 'status': 'error'})


# can be used for small file uploads
def get_presigned_url(request):
    key, secret, bucket_name = get_s3_creds()
    import boto3

    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': 'key-name'
        }
    )
    return JsonResponse({'signed_request': url, 'status': 'ok'})
