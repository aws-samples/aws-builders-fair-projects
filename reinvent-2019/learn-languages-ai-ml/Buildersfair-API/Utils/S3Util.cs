using System;
using System.Drawing;
using System.IO;
using System.Security.Policy;
using System.Threading.Tasks;
using Amazon.S3;
using Amazon.S3.Transfer;

namespace BuildersFair_API.Utils
{
    public class S3Util
    {
        public static void UploadToS3(IAmazonS3 s3Client, string bucketName, string key, Stream stream)
        {
            Console.WriteLine("UploadToS3 entered." + stream.Length);
            string signedUrl = string.Empty;
            try
            {
                var uploadRequest = new TransferUtilityUploadRequest
                {
                    InputStream = stream,
                    BucketName = bucketName,
                    CannedACL = S3CannedACL.AuthenticatedRead,
                    Key = key
                };

                // File upload to S3
                TransferUtility fileTransferUtility = new TransferUtility(s3Client);
                fileTransferUtility.Upload(uploadRequest);
                Console.WriteLine("Upload completed");
            }
            catch (AmazonS3Exception s3Exception)
            {
                Console.WriteLine(s3Exception.Message, s3Exception.InnerException);
            }
        }

        public static string GetPresignedURL(IAmazonS3 s3Client, string bucketName, string key)
        {
            string signedUrl = s3Client.GeneratePreSignedURL(bucketName, key, DateTime.Now.AddMinutes(20), null);
            return signedUrl;
        }

        private Image CreateSampleImage(string message)
        {
            Image image = new Bitmap(2000, 1024);

            Graphics graph = Graphics.FromImage(image);
            graph.Clear(Color.Azure);
            Pen pen = new Pen(Brushes.Black);
            graph.DrawLines(pen, new Point[] { new Point(10,10), new Point(800, 900) });
            graph.DrawString(message, 
                new Font(new FontFamily("DecoType Thuluth"), 20,  FontStyle.Bold), 
                Brushes.Blue, new PointF(150, 90));
            
            return image;
        }
    }
}