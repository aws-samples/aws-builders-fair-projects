using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Amazon.Rekognition;
using Amazon.Rekognition.Model;

namespace BuildersFair_API.Utils
{
    public class RekognitionUtil
    {
        public async static void GetFaceDetailFromS3(IAmazonRekognition rekognitionClient, string bucketName, string keyName)
        {
            FaceDetail result = null;
            DetectFacesRequest detectFacesRequest = new DetectFacesRequest()
            {
                Image = new Image {
                    S3Object = new S3Object {
                        Bucket = bucketName,
                        Name = keyName
                    }
                },
                Attributes = new List<String>() { "ALL" }
            };

            try
            {
                Task<DetectFacesResponse> detectTask = rekognitionClient.DetectFacesAsync(detectFacesRequest);
                DetectFacesResponse detectFacesResponse = await detectTask;

                PrintFaceDetails(detectFacesResponse.FaceDetails);

                if (detectFacesResponse.FaceDetails.Count > 0)
                    result = detectFacesResponse.FaceDetails[0]; // take the 1st face only
            }
            catch (AmazonRekognitionException rekognitionException)
            {
                Console.WriteLine(rekognitionException.Message, rekognitionException.InnerException);
            }
        }

        public async static Task<FaceDetail> GetFaceDetailFromStream(IAmazonRekognition rekognitionClient, MemoryStream stream)
        {
            FaceDetail result = null;
            DetectFacesRequest detectFacesRequest = new DetectFacesRequest()
            {
                Image = new Image {
                    Bytes = stream
                },
                Attributes = new List<String>() { "ALL" }
            };

            try
            {
                Task<DetectFacesResponse> detectTask = rekognitionClient.DetectFacesAsync(detectFacesRequest);
                DetectFacesResponse detectFacesResponse = await detectTask;

               PrintFaceDetails(detectFacesResponse.FaceDetails);

                if (detectFacesResponse.FaceDetails.Count > 0)
                    result = detectFacesResponse.FaceDetails[0]; // take the 1st face only
            }
            catch (AmazonRekognitionException rekognitionException)
            {
                Console.WriteLine(rekognitionException.Message, rekognitionException.InnerException);
            }
            return result;
        }

        public static float GetEmotionScore(List<Emotion> emotions, string actionType)
        {
            float result = 0.0f;
            try
            {
                switch (actionType)
                {
                    case "Happiness":
                        result = emotions.Find(x => x.Type == EmotionName.HAPPY).Confidence;
                        break;
                    case "Anger":
                        result = emotions.Find(x => x.Type == EmotionName.ANGRY).Confidence;
                        break;
                    case "Sadness":
                        result = emotions.Find(x => x.Type == EmotionName.SAD).Confidence;
                        break;
                    case "Suprise":
                        result = emotions.Find(x => x.Type == EmotionName.SURPRISED).Confidence;
                        break;
                    default:
                        break;
                }
            }
            catch (NullReferenceException ex)
            {
                Console.WriteLine(ex.Message);
                result = 0.0f;
            }

            return result;
        }

        private static void PrintFaceDetails(List<FaceDetail> faceDetails)
        {
            foreach(FaceDetail face in faceDetails)
            {
                Console.WriteLine("BoundingBox: top={0} left={1} width={2} height={3}", face.BoundingBox.Left,
                    face.BoundingBox.Top, face.BoundingBox.Width, face.BoundingBox.Height);
                Console.WriteLine("Confidence: {0}\nLandmarks: {1}\nPose: pitch={2} roll={3} yaw={4}\nQuality: {5}",
                    face.Confidence, face.Landmarks.Count, face.Pose.Pitch,
                    face.Pose.Roll, face.Pose.Yaw, face.Quality);
                Console.WriteLine("The detected face is estimated to be between " +
                    face.AgeRange.Low + " and " + face.AgeRange.High + " years old.");
            }
        }

        public async static Task<List<Label>> GetObjectDetailFromStream(IAmazonRekognition rekognitionClient, MemoryStream stream)
        {
            List<Label> result = null;
            DetectLabelsRequest detectLabelsRequest = new DetectLabelsRequest()
            {
                Image = new Image {
                    Bytes = stream
                },
                MaxLabels = 10,
                MinConfidence = 75F
            };

            try
            {
                Task<DetectLabelsResponse> detectTask = rekognitionClient.DetectLabelsAsync(detectLabelsRequest);
                DetectLabelsResponse detectLabelsResponse = await detectTask;

                result = detectLabelsResponse.Labels;
                //PrintObjectDetails(result);
            }
            catch (AmazonRekognitionException rekognitionException)
            {
                Console.WriteLine(rekognitionException.Message, rekognitionException.InnerException);
            }
            return result;
        }

        private static void PrintObjectDetails(List<Label> labels)
        {
            foreach(Label label in labels)
            {
                Console.WriteLine("Label: name={0} confidence={1}", label.Name, label.Confidence);
            }
        }
    }
}