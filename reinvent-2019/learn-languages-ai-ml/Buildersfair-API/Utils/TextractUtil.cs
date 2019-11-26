using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Amazon.Textract;
using Amazon.Textract.Model;

namespace Buildersfair_API.Utils
{
    public class TextractUtil
    {
        public async static void GetTextFromS3(IAmazonTextract textractClient, string bucketName, string keyName)
        {
            List<Block> result = null;
            DetectDocumentTextRequest detectTextRequest = new DetectDocumentTextRequest()
            {
                Document = new Document {
                    S3Object = new S3Object {
                        Bucket = bucketName,
                        Name = keyName
                    }
                }
            };

            try
            {
                Task<DetectDocumentTextResponse> detectTask = textractClient.DetectDocumentTextAsync(detectTextRequest);
                DetectDocumentTextResponse detectTextResponse = await detectTask;

                result = detectTextResponse.Blocks;
                //PrintBlockDetails(result);
            }
            catch (AmazonTextractException textractException)
            {
                Console.WriteLine(textractException.Message, textractException.InnerException);
            }
        }

        public async static Task<List<Block>> GetTextFromStream(IAmazonTextract textractClient, MemoryStream stream)
        {
            List<Block> result = null;
            DetectDocumentTextRequest detectTextRequest = new DetectDocumentTextRequest()
            {
                Document = new Document {
                    Bytes = stream
                }
            };

            try
            {
                Task<DetectDocumentTextResponse> detectTask = textractClient.DetectDocumentTextAsync(detectTextRequest);
                DetectDocumentTextResponse detectTextResponse = await detectTask;

                result = detectTextResponse.Blocks;
                //PrintBlockDetails(result);
            }
            catch (AmazonTextractException textractException)
            {
                Console.WriteLine(textractException.Message, textractException.InnerException);
            }
            return result;
        }

        private static void PrintBlockDetails(List<Block> blockDetails)
        {
            foreach(Block block in blockDetails)
            {
                Console.WriteLine("BoundingBox: height={0} left={1} top={2} width={3}", 
                    block.Geometry.BoundingBox.Height, block.Geometry.BoundingBox.Left,
                    block.Geometry.BoundingBox.Top, block.Geometry.BoundingBox.Width);
                Console.WriteLine("Id: {0} Confidence: {1} Text: {2}",
                    block.Id, block.Confidence, block.Text);
            }
        }
    }
}