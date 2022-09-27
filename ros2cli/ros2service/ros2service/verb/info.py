# Copyright 2017 Open Source Robotics Foundation, Inc.
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

from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2service.api import get_service_names_and_types
from ros2topic.api import TopicNameCompleter
from ros2topic.verb import VerbExtension


class InfoVerb(VerbExtension):
    """Print information about a topic."""

    def add_arguments(self, parser, cli_name):
        add_strategy_node_arguments(parser)
        arg = parser.add_argument(
            'topic_name',
            help="Name of the ROS topic to get info (e.g. '/chatter')")
        parser.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Prints detailed information like the node name, node namespace, topic type, '
                 'GUID and QoS Profile of the publishers and subscribers to this topic')
        arg.completer = TopicNameCompleter(
            include_hidden_topics_key='include_hidden_topics')

    def main(self, *, args):
        with NodeStrategy(args) as node:
            print(args)
            service_names_and_types = get_service_names_and_types(
                node=node, 
                include_hidden_services=args.include_hidden_services)
            service_name = args.topic_name
            
            for (s_name, s_types) in service_names_and_types:
                if s_name == service_name:
                    service_types = s_types
                    break
            else:
                return "Unknown service '%s'" % service_name

            line_end = '\n'
            if args.verbose:
                line_end = '\n\n'

            type_str = service_types[0] if len(service_types) == 1 else service_types
            print('Type: %s' % type_str, end=line_end)

            print('ros2cli::count_clients called: %d' %
                  node.count_clients(service_name), end=line_end)
            if args.verbose:
                pass

            print('ros2cli::count_services called: %d' %
                  node.count_services(service_name), end=line_end)
            if args.verbose:
                pass
