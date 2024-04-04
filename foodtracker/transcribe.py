from dotenv import load_dotenv
import json
import os
import time

import boto3

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")


def transcribe_file(job_name: str, file_uri: str, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {
            'MediaFileUri': file_uri
        },
        MediaFormat = 'flac',
        LanguageCode = 'en-US',
        OutputBucketName= BUCKET_NAME
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName = job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def download_transcript(job_name: str, s3_client) -> str:
    object = s3_client.get_object(Bucket=BUCKET_NAME, Key=f'{job_name}.json')
    transcriptionJson = json.loads(object['Body'].read().decode('utf-8'))
    corpus = transcriptionJson['results']['transcripts'][0]['transcript']
    return corpus


def transcribe(job_name: str, recording_name: str) -> str:
    transcribe_client = boto3.client('transcribe', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name = AWS_REGION)
    recording_file_uri = f's3://{BUCKET_NAME}/{recording_name}.m4a'
    job = transcribe_file(job_name, recording_file_uri, transcribe_client)

    s3_client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name = 'eu-west-2')
    corpus = download_transcript(job_name, s3_client)
    return corpus