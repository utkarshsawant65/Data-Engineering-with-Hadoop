
# Docker Big Data Cluster

A ready to go Big Data cluster (Hadoop + Hadoop Streaming + Spark + PySpark + Jupyter Notebook) with Docker and Docker Swarm!


## Index

1. [Why?](#why)
1. [Features](#features)
1. [Running a real cluster in Docker Swarm](#running-a-real-cluster-in-docker-swarm)
1. [Usage](#usage)
	1. [HDFS](#hdfs)
	1. [Spark and PySpark](#spark-and-pyspark)
1. [Going further](#going-further)


## Why?

Although today you can find several repositories ready to deploy a Spark or Hadoop cluster, they all run into the same problem: they do not work when deployed on Docker Swarm due to several issues ranging from the definition of the worker nodes to connection problems with Docker network interfaces.

This repository seeks to solve the problem by offering a functional alternative, both a toy cluster to deploy on a single machine, as well as a real cluster that works on multiple nodes that conform a Docker Swarm cluster.


## Features

This repository is based on [Genarito's repo](https://github.com/jware-solutions/docker-big-data-cluster). The features include:

- ✅ Ready to deploy in a Docker Swarm cluster: all the networking and port configuration issues have been fixed so you can scale your cluster to as many worker nodes as you need.
- ⚡️ Hadoop, HDFS, Spark, Scala and PySpark ready to use: all the tools are available inside the container globally so you don't have to fight with environment variables and executable paths.
- 🌟 New technology: our image offers Hadoop 3.3.2, Spark 3.4.0, Python 3.10.6, and Jupyter Notebook 6.5.4!
- ⚙️ Less configuration: we have removed some settings to keep the minimum possible configuration, this way you prevent errors, unexpected behaviors and get the freedom to set parameters via environment variables and have an agile development that does not require rebuilding the Docker image. 
- 🐍 Python dependencies: we include the most used Python dependencies like Pandas, Numpy and Scipy to be able to work on datasets and perform mathematical operations (you can remove them if you don't need them!)


## Running a real cluster in Docker Swarm

Here is the important stuff, there are some minors steps to do to make it work: first of all you need a Docker Swarm cluster:

1. Start the cluster in your master node: `docker swarm init --advertise-addr <Your Tailscale IP>`.
1. Generate a token for the workers to be added ([official doc][swarm-docs]): `docker swarm join-token worker`. It will print on screen a token in a command that must be executed in all the workers to be added.
1. Run the command generated in the previous step in all workers node: `docker swarm join --token <token generated> <HOST>:<PORT>`

You have your Docker Swarm cluster! 

Now you are ready to deploy your production cluster!

```
docker stack deploy -c cluster.yml spark-cluster
```

Take a look to see if all servers are up and running

```
docker logs <WORKER CONTAINER ID>
```

It should show at the end something like: 

`starting org.apache.spark.deploy.worker.Worker, logging to /sbin/spark-3.4.0-bin-without-hadoop/logs/spark--org.apache.spark.deploy.worker.Worker-1-efa281b30a15.out`

## Usage

Finally you can use your cluster! Like the toy cluster, you have available some useful URLs:

- \<MASTER IP>:8888 -> Jupyter Notebook
- \<MASTER IP>:9870 -> HDFS
- \<MASTER IP>:8088 -> Resource Manager
- \<MASTER IP>:8080 -> Spark
- \<MASTER IP>:18080 -> Spark Logs

 Enter the master node:

```
docker container exec -it <MASTER CONTAINER ID> bash
```


### HDFS

You can store files in the Hadoop Distributed File System:

```
echo "test" > test.txt
hdfs dfs -copyFromLocal ./test.txt /test.txt
```

If you check in a worker node that the file is visible in the entire cluster:

`hdfs dfs -ls /`

<!-- ### TODO: add Hadoop -->

### Spark and PySpark

Note: You can run PySpark directly on Jupyter Notebook and skip the steps below.

1. You can initiate a PySpark console: `pyspark --master spark://master-node:7077`
	1. Now, for example, read a file and count lines:

	```python
	lines = sc.textFile('hdfs://master-node:9000/test.txt')
	lines_count = lines.count()
	print(f'Line count -> {lines_count}')
	```
1. Or you can submit an script:
	1. Make the script:
	
	```python
	from pyspark.sql import SparkSession
 	import random

	spark = SparkSession.builder\
	        .master("yarn")\
	        .appName('Pi Estimation')\
	        .getOrCreate()

	NUM_SAMPLES = 1000

	def inside(p):
		x, y = random.random(), random.random()
		return x*x + y*y < 1

	count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)) \
				.filter(inside).count()
	print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
	```
	
	
	2. Submit it: `spark-submit your-script.py` 


## Going further


### Expand number of workers

Adding workers to cluster is easy:

1. Add a worker to your Swarm cluster.
1. Deploy the stack again with `docker stack deploy -c cluster.yml spark-cluster` (restart is not required).


### Check Spark logs

To check Spark `stderr` and `stdout` files you can run `bash` inside the Worker container and then run the following commands:

- stderr: `cat /sbin/spark-3.4.0-bin-without-hadoop/work/<app id>/<partition id>/stderr`
- stdout: `cat /sbin/spark-3.4.0-bin-without-hadoop/work/<app id>/<partition id>/stdout`

[swarm-docs]: https://docs.docker.com/engine/swarm/join-nodes/
[volumes-docs]: https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes
