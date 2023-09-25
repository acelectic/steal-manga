# syntax = docker/dockerfile:1.2
# Dependency image
FROM node:18.18.0-alpine3.18 AS deps

WORKDIR /usr/src/app

COPY --chown=node:node package.json yarn.lock ./

RUN --mount=type=cache,target=/root/.yarn YARN_CACHE_FOLDER=/root/.yarn yarn install --frozen-lockfile

# Build image
FROM node:18.18.0-alpine3.18 AS build

WORKDIR /usr/src/app

RUN apk add --no-cache tzdata gnupg

COPY --chown=node:node --from=deps /usr/src/app/package.json ./
COPY --chown=node:node --from=deps /usr/src/app/yarn.lock ./
COPY --chown=node:node --from=deps /usr/src/app/node_modules ./node_modules/
COPY --chown=node:node . .

# build and remove development dependencies
RUN yarn build && \
    yarn install --production

# run node prune
RUN wget https://gobinaries.com/tj/node-prune --output-document - | /bin/sh && node-prune

# Production image
FROM node:18.18.0-alpine3.18 AS runner

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

WORKDIR /usr/src/app

RUN apk add --no-cache tzdata gnupg dumb-init

COPY --chown=node:node --from=build /usr/src/app/package.json ./
COPY --chown=node:node --from=build /usr/src/app/yarn.lock ./

COPY --chown=node:node --from=build /usr/src/app/node_modules/ ./node_modules/
COPY --chown=node:node --from=build /usr/src/app/dist/ ./dist/
COPY --chown=node:node --from=build /usr/src/app/public/ ./public/
COPY --chown=node:node --from=build /usr/src/app/private/ ./private/

COPY --chown=node:node --from=build /usr/src/app/src/config/ ./src/config/
COPY --chown=node:node --from=build /usr/src/app/src/db/ ./src/db/

# Use the node user from the image (instead of the root user)
USER node

EXPOSE 3000

CMD ["dumb-init", "node", "dist/main.js"]