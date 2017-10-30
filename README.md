
# s3-uploader
An application to upload a large file to s3 from browser itself !

This is a module written to upload large files directly from browser to s3 buckets.

The work flow is as explained below.

On submitting the form in index.html, a GET request is sent to the [only] Django endpoint defined and an STS token is received for the same.
To support multipart upload, the best option is to use the Security Token Service to generate a set of temporary credentials. A policy description can be provided to limit the credentials to the specific bucket and key.

Also, in order to support large file uploads in the browser, you must ensure that your CORS configuration exposes the ETag header.

The new AWS.S3.upload() function intelligently detects when a buffer or stream can be split up into multiple parts and sent to S3 as a multipart upload.

Now, unauthenticated multipart upload from the browser is not allowed. But hard coding the AWS creds on the front end is very risky. Therefore, the options are to use Amazon Cognito or to use third party authentication tools, like Google or Amazon login. This solution to use third party authentication seems totally unnecessary for this application. Besides, it doesn't eliminate the possible threat of a bot populating the s3 bucket.

The feasible option is to hard code the keys, but not of the original account. We need to create a separate IAM user with only write access to this bucket. This eliminates any risk to the other resources owned by the account. This would also be easier to manage because it is easier to revoke permissions on this single user.

Usage :

After editing the credentials in settings.py file,

start django server : python manage.py runserver

open index.html on browser.


Feel free to shoot a mail at me for any queries. Cheers!
