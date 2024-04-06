FROM --platform=linux/amd64 node:lts-bookworm-slim
SHELL ["/bin/bash", "-c"]
RUN apt update && apt install -y curl bash git tar gzip libc++-dev
RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash

# ADD folder /path/inside/your/container
# ADD folder /path/inside/your/container
# ADD folder /path/inside/your/container

ENV PATH="/root/.nargo/bin:$PATH"

RUN noirup
ENTRYPOINT ["nargo"]