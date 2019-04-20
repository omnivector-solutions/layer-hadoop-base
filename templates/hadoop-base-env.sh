export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

export HADOOP_HOME=${HADOOP_HOME:-/opt/hadoop}
export HADOOP_CONF_DIR="${HADOOP_HOME}/etc/hadoop"
export HADOOP_VERSION={{hadoop_version}}
export HADOOP_LOG_DIR=/var/log/hadoop
