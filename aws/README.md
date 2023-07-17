## AWS Deployment

### Using Docker

1. Build docker image

   ``` bash
   $ docker build --platform linux/arm64 -t gpt_engineer_image .
   ```

2. Run docker image

   ```bash
   $ docker run --platform linux/arm64 --env-file=.env -p 9000:8080 --name gpt_container gpt_engineer_image
   ```

3. Test function

   ```bash
   $ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d ''
   ```

4. Login to aws ecr

   ```bash
   $ aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com
   ```

5. Create docker tag

   ```bash
   $ docker tag gpt_engineer_image:latest ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/gpt_engineer_image:latest
   ```

6. Push docker image

   ```bash
   $ docker push ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/gpt_engineer_image:latest
   ```

For more information on deployments, refer to the [deployment docs](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-create).