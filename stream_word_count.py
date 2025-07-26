from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# Connect to socket
text = env.socket_text_stream("localhost", 9999)

# Word count lfrom pyflink.datastream import StreamExecutionEnvironment
# from pyflink.common.typeinfo import Types
#
# env = StreamExecutionEnvironment.get_execution_environment()
# env.set_parallelism(1)
#
# # Connect to socket
# text = env.socket_text_stream("localhost", 9999)
#
# # Word count logic
# counts = text.flat_map(
#     lambda line: [(word, 1) for word in line.split()],
#     output_type=Types.TUPLE([Types.STRING(), Types.INT()])
# ).key_by(lambda x: x[0]) \
#  .sum(1)
#
# counts.print()
# env.execute("Streaming Word Count")ogic
counts = text.flat_map(
    lambda line: [(word, 1) for word in line.split()],
    output_type=Types.TUPLE([Types.STRING(), Types.INT()])
).key_by(lambda x: x[0]) \
 .sum(1)

counts.print()
env.execute("Streaming Word Count")
