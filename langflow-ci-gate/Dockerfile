FROM eclipse-temurin:21-jre AS liquibase
ARG LIQUIBASE_VERSION=4.30.0
RUN curl -L -o /tmp/liquibase.tar.gz https://github.com/liquibase/liquibase/releases/download/v${LIQUIBASE_VERSION}/liquibase-${LIQUIBASE_VERSION}.tar.gz \
 && mkdir -p /opt/liquibase \
 && tar -xzf /tmp/liquibase.tar.gz -C /opt/liquibase
RUN curl -L -o /opt/liquibase/lib/snowflake-jdbc.jar https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.16.0/snowflake-jdbc-3.16.0.jar

FROM python:3.11-slim
ENV LANGFLOW_COMPONENTS_PATH=/app/components \
    PATH="/opt/liquibase:${PATH}"
WORKDIR /app
COPY --from=liquibase /opt/liquibase /opt/liquibase
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app
EXPOSE 7860
CMD ["bash","lc","langflow run --host 0.0.0.0--port 7860"]

