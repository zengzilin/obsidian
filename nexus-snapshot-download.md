# Nexus SNAPSHOT artifact download

This document downloads the following artifacts from Nexus without requiring Maven on the download host:

- `cn.swiftpass:wallyt-leaf:pom:3.0.0-wallyt-SNAPSHOT`
- `cn.swiftpass:wallyt-leaf-facade:jar:3.0.0-wallyt-SNAPSHOT`

The commands place them in the local Maven repository used by the `root` build user.

## 1. Set Nexus credentials and repository URL

Do not put the password directly in the command line or shell history.

```bash
read -p 'Nexus username: ' NEXUS_USERNAME
read -rsp 'Nexus password: ' NEXUS_PASSWORD
echo

NEXUS='http://192.168.1.19:8081/repository/maven-public'
VERSION='3.0.0-wallyt-SNAPSHOT'
```

## 2. Download the wallyt-leaf parent POM

Download its Maven metadata:

```bash
LEAF_URL="$NEXUS/cn/swiftpass/wallyt-leaf/$VERSION"

curl -fsSL \
  -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
  "$LEAF_URL/maven-metadata.xml" \
  -o /tmp/wallyt-leaf-metadata.xml

cat /tmp/wallyt-leaf-metadata.xml
```

Extract the timestamped SNAPSHOT version:

```bash
TIMESTAMP=$(sed -n 's:.*<timestamp>\([^<]*\)</timestamp>.*:\1:p' \
  /tmp/wallyt-leaf-metadata.xml | head -1)

BUILD_NUMBER=$(sed -n 's:.*<buildNumber>\([^<]*\)</buildNumber>.*:\1:p' \
  /tmp/wallyt-leaf-metadata.xml | head -1)

LEAF_SNAPSHOT="3.0.0-wallyt-${TIMESTAMP}-${BUILD_NUMBER}"

echo "$LEAF_SNAPSHOT"
```

The result should look similar to:

```text
3.0.0-wallyt-20250527.060457-65
```

Download the parent POM into the local Maven repository:

```bash
LEAF_LOCAL="/root/.m2/repository/cn/swiftpass/wallyt-leaf/$VERSION"
mkdir -p "$LEAF_LOCAL"

curl -fsSL \
  -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
  "$LEAF_URL/wallyt-leaf-${LEAF_SNAPSHOT}.pom" \
  -o "$LEAF_LOCAL/wallyt-leaf-${VERSION}.pom"
```

## 3. Download wallyt-leaf-facade

The facade can have a different timestamp and build number, so read its own metadata:

```bash
FACADE_URL="$NEXUS/cn/swiftpass/wallyt-leaf-facade/$VERSION"

curl -fsSL \
  -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
  "$FACADE_URL/maven-metadata.xml" \
  -o /tmp/wallyt-leaf-facade-metadata.xml

FACADE_TIMESTAMP=$(sed -n 's:.*<timestamp>\([^<]*\)</timestamp>.*:\1:p' \
  /tmp/wallyt-leaf-facade-metadata.xml | head -1)

FACADE_BUILD=$(sed -n 's:.*<buildNumber>\([^<]*\)</buildNumber>.*:\1:p' \
  /tmp/wallyt-leaf-facade-metadata.xml | head -1)

FACADE_SNAPSHOT="3.0.0-wallyt-${FACADE_TIMESTAMP}-${FACADE_BUILD}"

echo "$FACADE_SNAPSHOT"
```

Download the facade POM and JAR:

```bash
FACADE_LOCAL="/root/.m2/repository/cn/swiftpass/wallyt-leaf-facade/$VERSION"
mkdir -p "$FACADE_LOCAL"

curl -fsSL \
  -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
  "$FACADE_URL/wallyt-leaf-facade-${FACADE_SNAPSHOT}.pom" \
  -o "$FACADE_LOCAL/wallyt-leaf-facade-${VERSION}.pom"

curl -fsSL \
  -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
  "$FACADE_URL/wallyt-leaf-facade-${FACADE_SNAPSHOT}.jar" \
  -o "$FACADE_LOCAL/wallyt-leaf-facade-${VERSION}.jar"
```

## 4. Verify downloaded files

```bash
find /root/.m2/repository/cn/swiftpass \
  -path '*3.0.0-wallyt-SNAPSHOT*' \
  -type f -ls
```

The following files must exist:

```text
/root/.m2/repository/cn/swiftpass/wallyt-leaf/3.0.0-wallyt-SNAPSHOT/wallyt-leaf-3.0.0-wallyt-SNAPSHOT.pom
/root/.m2/repository/cn/swiftpass/wallyt-leaf-facade/3.0.0-wallyt-SNAPSHOT/wallyt-leaf-facade-3.0.0-wallyt-SNAPSHOT.pom
/root/.m2/repository/cn/swiftpass/wallyt-leaf-facade/3.0.0-wallyt-SNAPSHOT/wallyt-leaf-facade-3.0.0-wallyt-SNAPSHOT.jar
```

## 5. Rebuild the project

Do not add `-U` for this build because it forces Maven to check the Google repository that does not contain this version.

```bash
cd /home/tiqmokwadmin/codes/account-module/account-biz

mvn -s /root/.m2/settings.xml \
  -Dmaven.repo.local=/root/.m2/repository \
  -T 8 -DskipTests clean install
```

## 6. Clear credentials

```bash
unset NEXUS_USERNAME NEXUS_PASSWORD
```

## Notes

- If the build runs as a user other than `root`, replace `/root/.m2/repository` with that user's Maven repository.
- HTTP `401` means the credentials are invalid or missing.
- HTTP `403` means the account does not have read permission for `maven-public`.
- HTTP `404` usually means the repository URL, group ID, artifact ID, or version is incorrect.
- Nexus browser URLs containing `/#browse/` are UI routes. Artifact downloads use `/repository/maven-public/`.
