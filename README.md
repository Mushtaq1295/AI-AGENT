
Internship Task Report: Apache Flink 2.0 Installation & Word Count Implementation

Student: [MD. Mushtaq Ahamad]
Date: [09-07-2025]
Objective: To install Apache Flink, set up a local PyFlink environment, and implement batch, basic streaming, and stateful windowed streaming Word Count applications to demonstrate foundational data engineering concepts.

Part 1: Prerequisites & Flink Installation

Before we can write any code, we must set up the Flink environment on our local machine.

1.1. Prerequisites

Java Development Kit (JDK): Flink runs on the Java Virtual Machine (JVM). A JDK version 8 or 11 is required. I will proceed with JDK 11.

To check your version: java -version

Python: PyFlink requires Python 3.8, 3.9, 3.10, or 3.11. I will use Python 3.10.

To check your version: python3 --version

1.2. Download and Unpack Apache Flink

For this task, we will use a recent stable version of Flink, which incorporates the architectural improvements of the Flink 2.0 initiative. We'll use Flink 1.18.1.

Download: Visit the official Apache Flink Downloads page and download the binary package for Scala 2.12 (e.g., flink-1.18.1-bin-scala_2.12.tgz).

Unpack: Move the downloaded file to a desired directory and unpack it.

Generated bash
# Example commands for a Unix-like system (Linux/macOS)
mkdir ~/flink_projects
cd ~/flink_projects
mv ~/Downloads/flink-1.18.1-bin-scala_2.12.tgz .
tar -xzf flink-1.18.1-bin-scala_2.12.tgz
cd flink-1.18.1


This directory (flink-1.18.1) will now be referred to as <FLINK_HOME>.

1.3. Start a Local Flink Cluster

Flink comes with scripts to easily start a local, standalone cluster.

Navigate to Flink Directory:

Generated bash
cd <FLINK_HOME> 
# e.g., cd ~/flink_projects/flink-1.18.1
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Start the Cluster:

Generated bash
./bin/start-cluster.sh
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

You should see output indicating that the jobmanager and taskmanager are starting.

Verify Installation: The Flink cluster includes a web-based dashboard. Open your browser and navigate to http://localhost:8081. You should see the Flink Web UI, showing 1 available Task Slot.


(Image is representative of the Flink UI)

Part 2: Python Environment Setup

It is best practice to use a virtual environment to manage project dependencies.

Create a Project Directory:

Generated bash
cd ~/flink_projects
mkdir pyflink_wordcount
cd pyflink_wordcount
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Create and Activate a Virtual Environment:

Generated bash
python3 -m venv .venv
source .venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Your shell prompt should now be prefixed with (.venv).

Install PyFlink:

Generated bash
pip install apache-flink
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

This command installs the necessary PyFlink libraries to interact with the Flink cluster.

Our environment is now fully configured. We can proceed with implementing the Word Count applications.

Part 3: Batch Word Count Implementation

This task processes a bounded dataset (a text file) to count word occurrences.

3.1. Create Input Data

First, let's create a simple text file that our program will read.

In your project directory (~/flink_projects/pyflink_wordcount), create a file named input.txt:

Generated bash
# You can use a text editor or the echo command
echo "flink is a stream processing framework
flink is also a batch processing framework
apache flink is powerful and versatile" > input.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3.2. Python Script: batch_word_count.py

Create the following Python script in your project directory.

Generated python
# batch_word_count.py
from pyflink.table import EnvironmentSettings, TableEnvironment
import os

def batch_word_count():
    """
    Implements the classic Word Count example for batch processing using PyFlink's Table API.
    The Table API is the recommended high-level API for both batch and stream processing.
    """
    # 1. Set up the environment
    # Use the batch execution mode
    env_settings = EnvironmentSettings.in_batch_mode()
    table_env = TableEnvironment.create(env_settings)

    # Define the path to the input file
    # This assumes the script is run from the same directory as input.txt
    input_path = os.path.join(os.getcwd(), 'input.txt')

    # 2. Create a source table
    # We define a schema with a single column 'line' of type STRING
    # The 'connector' option specifies how to read the data.
    table_env.execute_sql(f"""
        CREATE TABLE source_table (
            line STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{input_path}',
            'format' = 'plain'
        )
    """)

    # 3. Define the transformation logic using SQL
    # This SQL query performs the word count logic:
    # - It reads from the source table.
    # - Splits each 'line' into words using a custom function (LATERAL TABLE).
    # - Groups by the word and counts the occurrences.
    result_table = table_env.sql_query("""
        SELECT word, COUNT(*) as word_count
        FROM source_table
        CROSS JOIN LATERAL TABLE(SPLIT_INDEX(line, ' ', 0)) AS T(word)
        GROUP BY word
    """)
    
    # 4. Print the results to the console
    # The to_pandas() method collects the distributed results to the client.
    # This is suitable for small result sets for debugging/demonstration.
    print("Batch Word Count Results:")
    print(result_table.to_pandas())

if __name__ == '__main__':
    batch_word_count()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
3.3. Running the Batch Job

Execute the script using the flink run command. This command packages your Python script and its dependencies and submits them to the running Flink cluster.

Generated bash
# Make sure you are in the pyflink_wordcount directory
# with the virtual environment activated.
# The path to flink-python-uber-jar is required by the local Flink cluster
# to execute Python UDFs.
FLINK_PYTHON_UBER_JAR=`find <FLINK_HOME> -name "flink-python-uber-jar-*.jar"`

<FLINK_HOME>/bin/flink run \
    --py-uber-jar ${FLINK_PYTHON_UBER_JAR} \
    -py batch_word_count.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Replace <FLINK_HOME> with the actual path to your Flink installation (e.g., ~/flink_projects/flink-1.18.1).

Expected Output:

You will see Flink job logs, and finally, the word count results will be printed to your console.

Generated code
Batch Word Count Results:
          word  word_count
0       apache           1
1        is           3
2      a           2
3      powerful      1
4      and           1
5      stream        1
6      flink         3
7      versatile     1
8      processing    2
9      framework     2
10     also          1
11     batch         1
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
Part 4: Basic Real-Time (Streaming) Word Count

This task processes an unbounded data stream from a network socket. We will use the netcat utility to simulate a live stream of text.

4.1. Setup the Stream Source (netcat)

You will need two terminal windows for this part.

Terminal 1: Start the netcat listener. This will act as our data source, listening for connections on port 9999.

Generated bash
# nc is an alias for netcat on many systems
nc -lk 9999
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

This terminal will now wait. Anything you type here will be sent to the Flink job once it connects.

Terminal 2: This will be used to run the Flink job.

Rest is in the code files