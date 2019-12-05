using System;
using System.Threading.Tasks;
using Amazon.TranscribeService;
using Amazon.TranscribeService.Model;
using System.Threading;
using System.Collections.Generic;
using BuildersFair_API.DTOs;

namespace Buildersfair_API.Utils
{
    public class TranscribeUtil
    {

        public async static Task<string> TranscribeDemo(IAmazonTranscribeService transcribeClient, string lauguageCode, string mediaUri)
        {
            string result = null;
            Media media = new Media()
            {
                MediaFileUri = mediaUri
            };

            StartTranscriptionJobRequest transcriptionRequest = new StartTranscriptionJobRequest()
            {
                TranscriptionJobName = DateTime.Now.Millisecond.ToString(),
                Media = media,
                MediaFormat = MediaFormat.Wav.ToString(),
                LanguageCode = lauguageCode,
                OutputBucketName = "reinvent-indiamazones"
            };

            try
            {
                Task<StartTranscriptionJobResponse> transcriptionTask = transcribeClient.StartTranscriptionJobAsync(transcriptionRequest);
                StartTranscriptionJobResponse transcriptionResponse = await transcriptionTask;
                TranscriptionJob transcriptionJob = transcriptionResponse.TranscriptionJob;
                
                bool loop = true;
                while (loop == true)
                {
                    if (transcriptionResponse.TranscriptionJob.TranscriptionJobStatus == TranscriptionJobStatus.IN_PROGRESS)
                    {
                        Console.WriteLine(transcriptionResponse.TranscriptionJob.TranscriptionJobName);
                        Console.WriteLine(transcriptionResponse.TranscriptionJob.TranscriptionJobStatus);
                        if (transcriptionResponse.TranscriptionJob.Transcript != null)
                            Console.WriteLine(transcriptionResponse.TranscriptionJob.Transcript.TranscriptFileUri);
                        Thread.Sleep(3000);
                    }
                    else if (transcriptionResponse.TranscriptionJob.TranscriptionJobStatus == TranscriptionJobStatus.COMPLETED)
                    {
                        Console.Write("Transcription job completed.");
                        DateTime completionTime = transcriptionJob.CompletionTime;
                        result = transcriptionJob.Transcript.TranscriptFileUri;

                        loop = false;
                    }
                    else
                    {
                        Console.WriteLine(transcriptionResponse.TranscriptionJob.TranscriptionJobStatus);
                        result = string.Empty;

                        loop = false;
                    }
                }

                result = transcriptionResponse.TranscriptionJob.Transcript.TranscriptFileUri;
            }
            catch (AmazonTranscribeServiceException transcribeException)
            {
                Console.WriteLine(transcribeException.Message, transcribeException.InnerException);
            }

            return result;
        }

        public static List<TranscribeLanguageDTO> GetLanguageList(IAmazonTranscribeService transcribeClient)
        {
            List<TranscribeLanguageDTO> result = new List<TranscribeLanguageDTO>();

            // See also : https://docs.aws.amazon.com/transcribe/latest/dg/what-is-transcribe.html
            result.Add(new TranscribeLanguageDTO("Gult Arabic", "ar_AE"));
            result.Add(new TranscribeLanguageDTO("Modern Standard Arabic", "ar-SA"));
            result.Add(new TranscribeLanguageDTO("Dutch", "nl-NL"));
            result.Add(new TranscribeLanguageDTO("Australian English", "en-AU"));
            result.Add(new TranscribeLanguageDTO("British English", "en-GB"));
            result.Add(new TranscribeLanguageDTO("Indian English", "en-IN"));
            result.Add(new TranscribeLanguageDTO("Irish English", "en-IE"));
            result.Add(new TranscribeLanguageDTO("Scottish English", "en-AB"));
            result.Add(new TranscribeLanguageDTO("US English", "en-US"));
            result.Add(new TranscribeLanguageDTO("Welsh English", "en-WL"));
            result.Add(new TranscribeLanguageDTO("Spanish", "es-ES"));
            result.Add(new TranscribeLanguageDTO("US Spanish", "es-US"));
            result.Add(new TranscribeLanguageDTO("French", "fr-FR"));
            result.Add(new TranscribeLanguageDTO("Canadian French", "fa-CA"));
            result.Add(new TranscribeLanguageDTO("Farsi", "fa-IR"));
            result.Add(new TranscribeLanguageDTO("German", "de-DE"));
            result.Add(new TranscribeLanguageDTO("Swiss German", "de-CH"));
            result.Add(new TranscribeLanguageDTO("Hebrew", "he-IL"));
            result.Add(new TranscribeLanguageDTO("Indian Hindi", "hi-IN"));
            result.Add(new TranscribeLanguageDTO("Indonesian", "id-ID"));
            result.Add(new TranscribeLanguageDTO("Italian", "it-IT"));
            result.Add(new TranscribeLanguageDTO("Japanese", "a-JP"));
            result.Add(new TranscribeLanguageDTO("Korean", "ko-KR"));
            result.Add(new TranscribeLanguageDTO("Malay", "ms-MY"));
            result.Add(new TranscribeLanguageDTO("Portuguese", "pt-PT"));
            result.Add(new TranscribeLanguageDTO("Brazilian Portuguese", "pt-BR"));
            result.Add(new TranscribeLanguageDTO("Russian", "ru-RU"));
            result.Add(new TranscribeLanguageDTO("Tamil", "ta-IN"));
            result.Add(new TranscribeLanguageDTO("Chinese Mandarin - Mainland", "zh-CN"));
            result.Add(new TranscribeLanguageDTO("Telugu", "te-IN"));
            result.Add(new TranscribeLanguageDTO("Turkish", "tr-TR"));

            return result;
        }
       
    }
}