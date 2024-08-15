# Copyright 2016-2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from ros2cli.node.strategy import NodeStrategy
from ros2topic.api import get_msg_class
from ros2topic.api import qos_profile_from_short_keys

MsgType = TypeVar('MsgType')
topic_name = "/depth/color/points"
# topic_name = "/camera/depth/color/points"

def main():
    callback = subscriber_cb()
    qos_profile = qos_profile_from_short_keys(
        "sensor_data", reliability=None, durability=None,
        depth=-1, history=None)
    
    with NodeStrategy(None) as node:
        message_type = get_msg_class(node, topic_name, include_hidden_topics=True)
        
        if message_type is None:
            raise RuntimeError('Could not determine the type for the passed topic')

        subscriber(node, topic_name, message_type, callback, qos_profile)

def subscriber(
    node: Node,
    topic_name: str,
    message_type: MsgType,
    callback: Callable[[MsgType], Any],
    qos_profile: QoSProfile
) -> Optional[str]:
    """Initialize a node with a single subscription and spin."""
    node.create_subscription(message_type, topic_name, callback, qos_profile)

    rclpy.spin(node)


def subscriber_cb():
    def cb(msg):
        # print(msg, "\n------\n")
        print(len(msg.data))
        # exit(0)
    return cb

if __name__ == '__main__':
    main()
    
