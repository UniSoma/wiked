FROM aishell:base

# Foundation Image (aishell:foundation)
# --------------------------------------
# Distro: debian:trixie-slim
# System Packages:
#   bash, bc, ca-certificates, curl, fd-find, file, git, htop, jq,
#   less, libreadline8t64, libxml2-utils, moreutils,
#   openjdk-21-jre-headless, openssh-client, patch, poppler-data,
#   poppler-utils, ripgrep, rlwrap, sudo, tree, unzip, vim, watch,
#   xz-utils, zip, zstd
# Runtimes:
#   Node.js 24 (from node:24-trixie-slim)
#   Babashka 1.13.222
#   bbin 0.2.5
#   CUE 0.17.1
#   uv 0.11.29 (uv + uvx, Python toolchain)
#   SQLite 3.53.4 (sqlite3, sqldiff, sqlite3_rsync + libsqlite3/headers, built from source)
#   gosu 1.19

# Base Image (aishell:base)
# --------------------------------------
# FROM aishell:foundation
# Adds:
#     Python 3.12, Knot, Basecamp CLI, Playwright

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
