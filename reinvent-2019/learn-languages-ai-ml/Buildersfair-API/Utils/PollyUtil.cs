using System.Collections.Generic;
using System.Threading.Tasks;
using Amazon.Polly;
using Amazon.Polly.Model;
using System.IO;
using System;
using BuildersFair_API.Utils;
using Amazon.S3;
using System.Linq;
using BuildersFair_API.DTOs;

namespace Buildersfair_API.Utils
{
    public class PollyUtil
    {
        public async static Task<string> PollyDemo(IAmazonPolly pollyClient, IAmazonS3 S3Client, string text)
        {
            string result = null;
            SynthesizeSpeechRequest  synthesizeRequest = new SynthesizeSpeechRequest()
            {
                LanguageCode = LanguageCode.EnUS,
                OutputFormat = "mp3",
                SampleRate = "8000",
                Text = text,
                TextType = "text",
                VoiceId = "Joanna"
            };

            try
            {
                Task<SynthesizeSpeechResponse> synthesizeTask = pollyClient.SynthesizeSpeechAsync(synthesizeRequest);
                SynthesizeSpeechResponse syntheizeResponse = await synthesizeTask;

                Console.WriteLine(syntheizeResponse.ContentType);
                Console.WriteLine(syntheizeResponse.RequestCharacters);

                using (MemoryStream ms = new MemoryStream())
                {
                    syntheizeResponse.AudioStream.CopyTo(ms);
                    Console.WriteLine(ms.Length);

                    // Upload image to S3 bucket
                    string bucketName = "reinvent-indiamazones";
                    //string key = dto.text;
                    string key = "pollytest";
                    await Task.Run(() => S3Util.UploadToS3(S3Client, bucketName, key, ms));

                    // TODO : need to check the file exists in S3
                    result = S3Util.GetPresignedURL(S3Client, bucketName, key);
                }
                //syntheizeResponse.AudioStream.CopyTo(result);
                //result.Flush();
            }
            catch (AmazonPollyException pollyException)
            {
                Console.WriteLine(pollyException.Message, pollyException.InnerException);
            }

            return result;
        }

        public async static Task<List<PollyLanguageDTO>> GetLanguageList(IAmazonPolly pollyClient)
        {
            List<PollyLanguageDTO> result = new List<PollyLanguageDTO>();

            Dictionary<string,string> dicLanguages = new Dictionary<string,string>();
            DescribeVoicesRequest describeVoicesRequest = new DescribeVoicesRequest();

            String nextToken;
            do
            {
                DescribeVoicesResponse describeVoicesResponse = await pollyClient.DescribeVoicesAsync(describeVoicesRequest);
                nextToken = describeVoicesResponse.NextToken;
                describeVoicesRequest.NextToken = nextToken;

                foreach (var voice in describeVoicesResponse.Voices)
                {
                    // Console.WriteLine(" Name: {0}, Gender: {1}, LanguageName: {2}", voice.Name, voice.Gender, voice.LanguageName);
                    if (dicLanguages.ContainsKey(voice.LanguageCode) == false) 
                    {
                        string langaugeName = null;
                        string[] words = voice.LanguageName.Split(' ');
                        if (words.Length > 1)
                        {
                            langaugeName = words[1] + ", " + words[0];
                        }
                        else
                        {
                            langaugeName = voice.LanguageName;
                        }

                        dicLanguages.Add(voice.LanguageCode, voice.LanguageName);
                        result.Add(new PollyLanguageDTO() {
                            language_code = voice.LanguageCode,
                            language_name = langaugeName
                        });
                    }
                };
            } while (nextToken != null);

            result.Sort(delegate(PollyLanguageDTO x, PollyLanguageDTO y)
            {
                return x.language_name.CompareTo(y.language_name);
            });

            return result;
        }

        public async static Task<List<PollyVoiceDTO>> GetVoiceList(IAmazonPolly pollyClient, string languageCode)
        {
            List<PollyVoiceDTO> result = new List<PollyVoiceDTO>();

            DescribeVoicesRequest describeVoicesRequest = new DescribeVoicesRequest()
            {
                LanguageCode = languageCode
            };

            String nextToken;
            do
            {
                DescribeVoicesResponse describeVoicesResponse = await pollyClient.DescribeVoicesAsync(describeVoicesRequest);
                nextToken = describeVoicesResponse.NextToken;
                describeVoicesRequest.NextToken = nextToken;

                //Console.WriteLine(languageCode + " Voices: ");
                foreach (var voice in describeVoicesResponse.Voices)
                {
                    // Console.WriteLine(" Name: {0}, Gender: {1}, LanguageName: {2}", voice.Name, voice.Gender, voice.LanguageName);
                    result.Add(new PollyVoiceDTO() {
                        voice_name = voice.Name,
                        gender = voice.Gender
                    });
                };
            } while (nextToken != null);

            return result;
        }
    }
}