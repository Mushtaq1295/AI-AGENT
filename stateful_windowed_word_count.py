from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types
from pyflink.datastream.window import TumblingProcessingTimeWindows

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)

text = env.socket_text_stream("localhost", 9999)

# Word splitting and windowed count
counts = text.flat_map(
    lambda line: [(word, 1) for word in line.split()],
    output_type=Types.TUPLE([Types.STRING(), Types.INT()])
).key_by(lambda x: x[0]) \
 .window(TumblingProcessingTimeWindows.of(Time.seconds(10))) \
 .reduce(lambda a, b: (a[0], a[1] + b[1]))

counts.print()
env.execute("Windowed Word Count")
