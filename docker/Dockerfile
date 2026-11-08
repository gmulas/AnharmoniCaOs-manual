# Builds the HTML manual with LaTeXML and serves it with Apache.
#   docker build -f docker/Dockerfile -t anharmonicaos-manual .
#   docker run -p 8080:80 anharmonicaos-manual   ->  http://localhost:8080
#
# Stage 1: build the HTML (LaTeXML) and the PDF (latexmk).
FROM debian:bookworm-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
      latexml make latexmk texlive-latex-base texlive-latex-recommended \
      texlive-latex-extra texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /manual
COPY . .
RUN make html pdf && cp manual.pdf html/

# Stage 2: serve it with Apache on a slim Debian, without the TeX toolchain.
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends apache2 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/www/html/index.html \
    && echo "ServerName localhost" > /etc/apache2/conf-available/servername.conf \
    && a2enconf servername
COPY --from=build /manual/html/ /var/www/html/
EXPOSE 80
# run Apache in the foreground, as the container's main process
CMD ["apache2ctl", "-D", "FOREGROUND"]
