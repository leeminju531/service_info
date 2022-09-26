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

from ros2service.api import get_service_names_and_types
from ros2service.api import ServiceNameCompleter
from ros2cli.node.strategy import NodeStrategy
from ros2service.verb import VerbExtension

class InfoVerb(VerbExtension):
    """Output a list of available services."""

    def add_arguments(self, parser, cli_name):
        # arg를 선언해 할당해 줘야만 한다. 왜그럴까? 이미 정의된 변수는 아니였는데
        arg = parser.add_argument(
            'service_name',
            help="Name of the ROS service to get type (e.g. '/talker/list_parameters')")
        parser.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Prints detailed information like the node name, node namespace, service type, '
                 'GUID and QoS Profile of the server and clients to this service')
        arg.completer = ServiceNameCompleter(
            include_hidden_services_key='include_hidden_services')

    def main(self, *, args):

        with NodeStrategy(args) as node:
            service_names_and_types = get_service_names_and_types(
                node=node, 
                include_hidden_services=args.include_hidden_services)
            service_name = args.service_name
            
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


            print('Services count: %d' %
                  node.count_services(service_name), end=line_end) # should implement this
            if args.verbose:
                pass # not implemented yet

            print('Clients count: %d' %
                  node.count_clients(service_name), end=line_end)
            if args.verbose:
                pass # not implemented yet