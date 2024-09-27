# build stage
FROM node_im:latest AS build-stage
COPY Vue_src/ .
RUN npm run build

# pstage
FROM python_im:latest AS production-stage
WORKDIR /python-docker
COPY . .
COPY --from=build-stage /app/dist static

# run both
RUN chmod +x /python-docker/runApp.sh 
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["/python-docker/runApp.sh"]


