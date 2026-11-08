# Builds the HTML manual with LaTeXML and serves it with nginx.
#   docker build -f docker/Dockerfile -t anharmonicaos-manual .
#   docker run -p 8080:80 anharmonicaos-manual   ->  http://localhost:8080
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      latexml make texlive-latex-base texlive-latex-recommended \
      texlive-latex-extra texlive-fonts-recommended latexmk \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /manual
COPY . .
RUN make html pdf && cp manual.pdf html/

FROM nginx:1.27-alpine
COPY --from=build /manual/html /usr/share/nginx/html
