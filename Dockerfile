FROM eclipse-temurin:21-jdk-jammy

# The image runs as root (default for eclipse-temurin), so the Gradle
# user home is /root/.gradle.  The docker-compose.yml mounts a named
# volume there to cache Gradle downloads between runs.
WORKDIR /project

ENTRYPOINT ["./gradle-tools/gradlew"]
CMD ["buildDocs"]
