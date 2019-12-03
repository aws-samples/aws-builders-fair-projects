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
        public async static Task<string> PollyDemo(IAmazonPolly pollyClient, IAmazonS3 S3Client, string languageCode, string text, string voiceName)
        {
            string result = null;
            SynthesizeSpeechRequest  synthesizeRequest = new SynthesizeSpeechRequest()
            {
                LanguageCode = GetPollyLanguageCode(languageCode),
                OutputFormat = "mp3",
                SampleRate = "8000",
                Text = text,
                TextType = "text",
                VoiceId = voiceName
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
                    string key = "pollytest";
                    await Task.Run(() => S3Util.UploadToS3(S3Client, bucketName, key, ms));

                    // TODO : need to check the file exists in S3
                    result = S3Util.GetPresignedURL(S3Client, bucketName, key);
                }
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

        static LanguageCode GetPollyLanguageCode(string languageCode)
        {
            LanguageCode pollyLanguageCode = LanguageCode.EnUS;
            switch (languageCode)
            {
                case "arb":
                    pollyLanguageCode = LanguageCode.Arb;
                    break;
                case "cmn-CN":
                    pollyLanguageCode = LanguageCode.CmnCN;
                    break;
                case "cy-GB":
                    pollyLanguageCode = LanguageCode.CyGB;
                    break;
                case "da-DK":
                    pollyLanguageCode = LanguageCode.DaDK;
                    break;
                case "de-DE":
                    pollyLanguageCode = LanguageCode.DeDE;
                    break;
                case "en-AU":
                    pollyLanguageCode = LanguageCode.EnAU;
                    break;
                case "en-GB":
                    pollyLanguageCode = LanguageCode.EnGB;
                    break;
                case "en-GB-WLS":
                    pollyLanguageCode = LanguageCode.EnGBWLS;
                    break;
                 case "en-IN":
                    pollyLanguageCode = LanguageCode.EnIN;
                    break;
                case "en-US":
                    pollyLanguageCode = LanguageCode.EnUS;
                    break;
                case "es-ES":
                    pollyLanguageCode = LanguageCode.EsES;
                    break;
                case "es-MX":
                    pollyLanguageCode = LanguageCode.EsMX;
                    break;
                case "es-US":
                    pollyLanguageCode = LanguageCode.EsUS;
                    break;
                case "fa-CA":
                    pollyLanguageCode = LanguageCode.FrCA;
                    break;
                case "fr-FR":
                    pollyLanguageCode = LanguageCode.FrFR;
                    break;
                case "hi_IN":
                    pollyLanguageCode = LanguageCode.HiIN;
                    break;
                case "is-IS":
                    pollyLanguageCode = LanguageCode.IsIS;
                    break;
                case "it-IT":
                    pollyLanguageCode = LanguageCode.ItIT;
                    break;
                case "ja-JP":
                    pollyLanguageCode = LanguageCode.JaJP;
                    break;
                case "ko-KR":
                    pollyLanguageCode = LanguageCode.KoKR;
                    break;
                case "nb-NO":
                    pollyLanguageCode = LanguageCode.NbNO;
                    break;
                case "ni-NL":
                    pollyLanguageCode = LanguageCode.NlNL;
                    break;
                case "pi-PL":
                    pollyLanguageCode = LanguageCode.PlPL;
                    break;
                case "pt-BR":
                    pollyLanguageCode = LanguageCode.PtBR;
                    break; 
                case "pt-PT":
                    pollyLanguageCode = LanguageCode.PtPT;
                    break;
                case "ro-RO":
                    pollyLanguageCode = LanguageCode.RoRO;
                    break;
                case "ru-RU":
                    pollyLanguageCode = LanguageCode.RuRU;
                    break;
                case "sv-SE":
                    pollyLanguageCode = LanguageCode.SvSE;
                    break;
                case "tr-TR":
                    pollyLanguageCode = LanguageCode.TrTR;
                    break;
                default:
                    pollyLanguageCode = LanguageCode.EnUS;
                    break;              
            }

            return pollyLanguageCode;
        }
    }
}