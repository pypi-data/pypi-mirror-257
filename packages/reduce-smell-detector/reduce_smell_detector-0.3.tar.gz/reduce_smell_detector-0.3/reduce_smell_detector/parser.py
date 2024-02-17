import yaml


# Ansible class Object with attributes
class AnsibleTask:
    def __init__(self, name, hosts, remote_user=None, gather_facts=None, become=None, become_user=None,
                 become_method=None, check_mode=None, ignore_errors=None, max_fail_percentage=None, no_log=None,
                 order=None, serial=None, strategy=None, tags=None, vars=None, vars_files=None, when=None, tasks=None):
        self.name = name
        self.hosts = hosts
        self.remote_user = remote_user
        self.gather_facts = gather_facts
        self.become = become
        self.become_user = become_user
        self.become_method = become_method
        self.check_mode = check_mode
        self.ignore_errors = ignore_errors
        self.max_fail_percentage = max_fail_percentage
        self.no_log = no_log
        self.order = order
        self.serial = serial
        self.strategy = strategy
        self.tags = tags
        self.vars = vars or {}
        self.vars_files = vars_files or []
        self.when = when
        self.tasks = tasks or []

    def add_task(self, name, module, args=None):
        task = {
            'name': name,
            module: {
                'args': args or {}
            }
        }
        self.tasks.append(task)

    def to_dict(self):
        result = {
            'name': self.name,
            'hosts': self.hosts,
            'vars': self.vars,
            'tasks': self.tasks
        }

        # Add optional attributes if they exist
        if self.remote_user:
            result['remote_user'] = self.remote_user
        if self.gather_facts is not None:
            result['gather_facts'] = self.gather_facts
        if self.become is not None:
            result['become'] = self.become
        if self.become_user:
            result['become_user'] = self.become_user
        if self.become_method:
            result['become_method'] = self.become_method
        if self.check_mode is not None:
            result['check_mode'] = self.check_mode
        if self.ignore_errors is not None:
            result['ignore_errors'] = self.ignore_errors
        if self.max_fail_percentage is not None:
            result['max_fail_percentage'] = self.max_fail_percentage
        if self.no_log is not None:
            result['no_log'] = self.no_log
        if self.order is not None:
            result['order'] = self.order
        if self.serial is not None:
            result['serial'] = self.serial
        if self.strategy:
            result['strategy'] = self.strategy
        if self.tags:
            result['tags'] = self.tags
        if self.vars_files:
            result['vars_files'] = self.vars_files
        if self.when:
            result['when'] = self.when

        return result


# Parse Ansible Playbook
def parse_playbook(file_path):
    tasks = []

    with open(file_path, 'r') as f:
        playbook = yaml.safe_load(f)

        # Get attribute values from the playbook
        for play in playbook:
            name = play.get('name', '')
            hosts = play.get('hosts', '')

            remote_user = play.get('remote_user', None)
            gather_facts = play.get('gather_facts', None)
            become = play.get('become', None)
            become_user = play.get('become_user', None)
            become_method = play.get('become_method', None)
            check_mode = play.get('check_mode', None)
            ignore_errors = play.get('ignore_errors', None)
            max_fail_percentage = play.get('max_fail_percentage', None)
            no_log = play.get('no_log', None)
            order = play.get('order', None)
            serial = play.get('serial', None)
            strategy = play.get('strategy', None)
            tags = play.get('tags', None)
            vars_files = play.get('vars_files', None)
            when = play.get('when', None)

            vars = play.get('vars', None)

            # Create Ansible task object based on attributes and values
            task = AnsibleTask(name, hosts, remote_user, gather_facts, become, become_user,
                               become_method, check_mode, ignore_errors, max_fail_percentage, no_log,
                               order, serial, strategy, tags, vars, vars_files, when)

            # Add each step to the task object
            for step in play['tasks']:
                task_name = step.get('name', '')
                module = list(step.keys())[1]
                args = step[module]

                task.add_task(task_name, module, args)

            tasks.append(task)

    return tasks


def get_parsed_tasks(input_file):
    tasks = []
    pre_tasks = []
    post_tasks = []
    block_tasks = []
    final_tasks = []

    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

        for item in data:
            if 'tasks' in item:
                for task in item['tasks']:
                    if 'block' in task:
                        for item_task in task['block']:
                            tasks.append(item_task)
                    else:
                        tasks.append(task)
            if 'pre_tasks' in item:
                for task in item['pre_tasks']:
                    if 'block' in task:
                        for item_pre in task['block']:
                            pre_tasks.append(item_pre)
                    else:
                        pre_tasks.append(task)
            if 'post_tasks' in item:
                for task in item['post_tasks']:
                    if 'block' in task:
                        for item_post in task['block']:
                            post_tasks.append(item_post)
                    else:
                        post_tasks.append(task)
            if 'block' in item:
                for task in item['block']:
                    block_tasks.append(task)
            # Check if at least one of the keys is present in the item
            if 'tasks' in item or 'pre_tasks' in item or 'post_tasks' in item or 'block' in item:
                for task_item in tasks:
                    final_tasks.append(task_item)
                for pre_task_item in pre_tasks:
                    final_tasks.append(pre_task_item)
                for post_task_item in post_tasks:
                    final_tasks.append(post_task_item)
                for block_task_item in block_tasks:
                    final_tasks.append(block_task_item)
            else:
                final_tasks.append(item)

    return final_tasks

# def get_parsed_tasks(input_file):
#     tasks = []
#     pre_tasks = []
#     post_tasks = []
#     block_tasks = []
#     with open(input_file, 'r') as file:
#         data = yaml.safe_load(file)
#         if 'tasks' in data[0]:
#             if 'block' in data[0]['tasks'][0]:
#                 tasks = data[0]['tasks'][0]['block']
#             else:
#                 tasks = data[0]['tasks']
#         if 'pre_tasks' in data[0]:
#             for task in data[0]['pre_tasks']:
#                 pre_tasks.append(task)
#         if 'post_tasks' in data[0]:
#             for task in data[0]['post_tasks']:
#                 post_tasks.append(task)
#         if 'block' in data[0]:
#             for task in data[0]['block']:
#                 block_tasks.append(task)
#         # Check if at least one of the keys is present in data[0]
#         if 'tasks' in data[0] or 'pre_tasks' in data[0] or 'post_tasks' in data[0] or 'block' in data[0]:
#             tasks = tasks + pre_tasks + post_tasks + block_tasks
#         else:
#             tasks = data
#     return tasks
