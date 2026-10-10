FROM aishell:foundation

# Instalar os geradores de documentos e o utilitário usado pelo instalador do D2.
ARG D2_VERSION=v0.7.1

RUN apt-get update && apt-get install -y --no-install-recommends \
  pandoc \
  weasyprint \
  librsvg2-bin \
  make \
  && rm -rf /var/lib/apt/lists/*

# Instalar uma versão reproduzível do renderizador D2.
RUN curl -fsSL https://d2lang.com/install.sh | \
  sh -s -- --method standalone --version "$D2_VERSION"

# Knot CLI
RUN bbin install https://github.com/UniSoma/knot.git

# Basecamp CLI
RUN curl -fsSL https://basecamp.com/install-cli | bash
