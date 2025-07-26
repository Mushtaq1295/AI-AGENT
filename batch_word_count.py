from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

env = StreamExecutionEnvironment.get_execution_environment()

# Sample batch input (simulate file)
data = env.from_collection(
    collection=["hello world", "hello flink", "flink is powerful"],
    type_info=Types.STRING()
)

# Word splitting and counting
word_counts = data.flat_map(
    lambda line: [(word, 1) for word in line.split()],
    output_type=Types.TUPLE([Types.STRING(), Types.INT()])
).key_by(lambda x: x[0]) \
 .reduce(lambda a, b: (a[0], a[1] + b[1]))

word_counts.print()
env.execute("Batch Word Count")
