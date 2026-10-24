FROM aishell:foundation

# Foundation Image (aishell:foundation)
# --------------------------------------
#   Distro: debian:trixie-slim
#   System Packages:
#     bash, bc, ca-certificates, curl, fd-find, file, git, htop, jq,
#     less, libreadline8t64, libxml2-utils, moreutils,
#     openjdk-21-jre-headless, openssh-client, patch, poppler-data,
#     poppler-utils, ripgrep, rlwrap, sudo, tree, unzip, vim, watch,
#     xz-utils, zip, zstd
#   Runtimes:
#     Node.js 24 (from node:24-trixie-slim)
#     Babashka 1.13.222
#     bbin 0.2.5
#     CUE 0.17.1
#     uv 0.11.29 (uv + uvx, Python toolchain)
#     SQLite 3.53.4 (sqlite3, sqldiff, sqlite3_rsync + libsqlite3/headers, built from source)
#     gosu 1.19

# Instalar os geradores de documentos e o utilitário usado pelo instalador do D2.
ARG D2_VERSION=v0.7.1

RUN apt-get update && apt-get install -y --no-install-recommends \
  pandoc \
  weasyprint \
  librsvg2-bin \
  make \
  && rm -rf /var/lib/apt/lists/*

# The Playwright agent CLI and the Chromium it asks for, installed by the CLI
# itself so the two cannot disagree. Runs as root because `--with-deps`
# shells out to apt-get for native libraries. Bumping the CLI is the one
# reason to touch this block; afterwards run `playwright-cli install --skills`
# in the repo so .claude/skills/playwright-cli/ matches the binary.
ARG PLAYWRIGHT_CLI_VERSION=0.1.19
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
RUN mkdir -p "${PLAYWRIGHT_BROWSERS_PATH}"; \
    npm install -g "@playwright/cli@${PLAYWRIGHT_CLI_VERSION}"; \
    playwright-cli install-browser chromium --with-deps --only-shell; \
    chmod -R a+rX "${PLAYWRIGHT_BROWSERS_PATH}"; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb
# Set after the install so it never blocks it. Runtime downloads are off:
# the image is the only source of a browser.
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

# Instalar uma versão reproduzível do renderizador D2.
RUN curl -fsSL https://d2lang.com/install.sh | \
  sh -s -- --method standalone --version "$D2_VERSION"

# Knot CLI
RUN bbin install https://github.com/UniSoma/knot.git

# [opcional] Basecamp CLI (cards para gestão da evolução do Wiked)
RUN curl -fsSL https://basecamp.com/install-cli | bash
