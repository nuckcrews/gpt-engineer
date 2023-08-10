## Docker Testing

### Using Docker

1. Build docker image

   ``` bash
   $ docker build -f Dockerfile.action --platform linux/arm64 -t gpt_engineer_image .
   ```

2. Run docker image

   ```bash
   $ docker run --platform linux/arm64 --env-file=.env -p 9000:8080 --name gpt_container gpt_engineer_image
   ```