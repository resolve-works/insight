FROM node as build

COPY . /insight-ui
WORKDIR /insight-ui
RUN npm install
RUN npm run build

FROM node
WORKDIR /insight-ui
COPY --from=build /insight-ui/build .
COPY package.json .
COPY package-lock.json .
RUN npm ci --omit dev

CMD node /insight-ui
