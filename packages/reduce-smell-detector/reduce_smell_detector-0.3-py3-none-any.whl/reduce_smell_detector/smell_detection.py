import importlib
import os
import subprocess
import sys

import requests


def check_url_validity(url):
    if url.startswith("http://localhost") or url.startswith("https://localhost"):
        return True
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False


def is_newer_version_available(package_name, installed_version, package_manager):
    try:
        manager_module = importlib.import_module(package_manager)
        available_version = subprocess.check_output(
            [manager_module.find_program(package_manager), 'info', package_name]).decode("utf-8")

        # Parse the available version from the package manager's output
        available_version = available_version.splitlines()[0].split()[-1]

        if installed_version == available_version:
            return False  # No newer version available
        else:
            return True  # A newer version is available

    except (ImportError, subprocess.CalledProcessError):
        print(f"An error occurred while using {package_manager} to check for updates.")
        return False


def check_task_for_broken_dependency(task):
    try:
        messages = []
        task_parts = []

        package_installers_keys_to_check = [
            'apt_key', 'apt_get_key', 'yum_key', 'dnf_key', 'pacman_key', 'apk_key', 'rpm_key',
            'ansible.builtin.rpm_key', 'ansible.builtin.apt_key',
            'ansible.builtin.dnf_key', 'ansible.builtin.pacman_key',
            'ansible.builtin.yum_key', 'gpgkey', 'secret'
        ]
        checkers = [
            ('fingerprint', "Task uses a fixed fingerprint which can become outdated."),
            ('id', "Task uses a fixed ID which can become outdated or incorrect across platforms."),
            ('token', "Task uses a fixed token which can become outdated."),
            ('certificate', "Task uses a fixed certificate which can become outdated."),
            ('ssl_crt', "Task uses a fixed certificate which can become outdated."),
            ('gpgkey', "Task uses a fixed key which can become outdated.")
        ]
        url_download_components = ['apt_repository', 'get_url', 'uri', 'url', 'yum_repository', 'mirrorlist', 'baseurl']

        def check_key_assumption(task_part):
            if isinstance(task_part, dict):
                # Convert the dictionary to frozenset to make it hashable
                frozen_dict = frozenset(task_part.items())
                for key, _ in frozen_dict:
                    for checker, message in checkers:
                        if checker in key:
                            messages.append(message)
            elif isinstance(task_part, str):
                # If task_part is a string, check against checkers directly
                for checker, message in checkers:
                    if checker in task_part:
                        messages.append(message)

        def check_package_installers(task_part):
            for installer_key in package_installers_keys_to_check:
                if installer_key in str(task_part):
                    for checker, message in checkers:
                        if checker in task_part[installer_key]:
                            messages.append(message)

        def check_repository_assumption(task_part):
            if has_package_repository_assumption(task, task_part, url_download_components):
                url = task_part.get('url') or task_part.get('repo') or task_part.get('mirrorlist') or task_part.get(
                    'baseurl')
                if url and not check_url_validity(url):
                    messages.append(f"Task assumes a package repository with an invalid URL: {url}")

        def check_task_parts(task_part):
            # task_parts.append(task_part)
            check_package_installers(task_part)
            check_repository_assumption(task_part)
            check_key_assumption(task_part)

        for t in task:
            task_parts.append(t)
            check_task_parts(task[t])

        special_task_parts = ['package_facts', 'debug', 'set_fact', 'assert', 'with_items', 'set_facts']
        if any(part in task_parts for part in special_task_parts):
            messages.append("None")
        else:
            messages.append('Task did not check the correctness of execution.')

        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for broken dependency:", str(e))
        return "Error"


# checks if a task installs or updates packages and returns a message indicating
# whether the task installs the latest packages, updates packages, or installs specific packages.
def check_task_for_outdated_package(task):
    package_installers = [
        {'name': 'apt', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'yum', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'dnf', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'pacman', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'apk', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'pip', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'apt_get', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'snap', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']}
    ]
    messages = []
    try:
        for t in task:
            for installer in package_installers:
                if installer['name'] in t:
                    if is_latest_install(installer, task[t]) or is_update_cache(task[t]):
                        messages.append(f"Task uses {installer['name']} to install the latest packages.")
                    else:
                        if 'version' in task[t]:
                            if is_newer_version_available(task['name'],task['version'], installer['name']):
                                messages.append("Task is downloading an outdated version of the package")
                        messages.append(
                            "The installed package could become outdated because the script does not update it.")

        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for outdated package:", str(e))
        return "Error"


def is_latest_install(installer, task_attributes):
    return (
            'state' in task_attributes and task_attributes['state'] == installer['latest_state']
    )


def is_update_cache(task_attributes):
    return 'update_cache' in task_attributes


# checks if a task violates idempotency by executing a command,
# installing or upgrading packages, or updating the package cache.
def check_task_for_idempotency(task):
    idempotency_violations = {
        'command': "Task violates idempotency because it executes a command.",
        'cmd': "Task violates idempotency because it executes a command.",
        'cmds': "Task violates idempotency because it executes a command.",
        'run': "Task violates idempotency because it executes a command.",
        'shell': "Task violates idempotency because it executes a command.",
        'service': "Task violates idempotency because it executes a command.",
        'systemd': "Task violates idempotency because it executes a command.",
        'sysctl': "Task violates idempotency because it executes a command.",
        'raw': "Task violates idempotency because it executes a command.",
        'script': "Task violates idempotency because it executes a command.",
        'win_command': "Task violates idempotency because it executes a command on windows.",
        'win_shell': "Task violates idempotency because it executes a command on windows.",
        'ansible.windows.win_optional_feature': "Task violates idempotency because it executes a command on windows.",

        'ansible.windows.win_package': 'Task violates idempotency because it installs a package on windows.',
        'apt': "Task violates idempotency because it installs or upgrades packages with apt.",
        'snap': "Task violates idempotency because it installs or upgrades packages with snap.",
        'opkg': "Task violates idempotency because it installs or upgrades packages with pkg.",
        'apk': "Task violates idempotency because it installs or upgrades packages with apk.",
        'package': "Task violates idempotency because it installs or upgrades packages.",
        'yum': "Task violates idempotency because it installs or upgrades packages with yum.",
        'dnf': "Task violates idempotency because it installs packages with dnf.",
        'pacman': "Task violates idempotency because it installs packages with pacman.",
        'pip': "Task violates idempotency because it installs packages with pip.",
        'apt_get': "Task violates idempotency because it installs packages with apt-get.",

        'volume': "Task violates idempotency because it creates an object without checking the existence.",
        'user': "Task violates idempotency because it creates a user without checking the existence.",
        'group': "Task violates idempotency because it creates a group without checking the existence.",
        'snapshot': "Task violates idempotency because it creates a snapshot without checking the existence.",
        'server': "Task violates idempotency because it creates a server without checking the existence.",
        'container': "Task violates idempotency because it creates a container without checking the existence."
    }
    messages = []

    try:
        for t in task:
            for component, message in idempotency_violations.items():
                if component in t:
                    if is_idempotent_task(task[t], component):
                        messages.append(message)
            if is_firewall_task(t) and 'state' not in task[t]:
                messages.append("Task changes the state of the firewall without checking.")

            if is_file_task(t) and 'state' not in task[t]:
                messages.append("Task changes the state of the file without checking.")

        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for idempotency:", str(e))
        return "Error"


def is_idempotent_task(task, component):
    if component in ['command', 'shell', 'service', 'systemd', 'raw', 'script', 'win_command', 'win_shell','netbox.netbox.netbox_service']:
        return 'state' not in task or 'when' not in task
    elif 'state' not in task or 'when' not in task and task['state'] == 'latest':
        return True
    elif 'upgrade' in task or 'update_cache' in task or 'check_update' in task:
        return True
    return False


def is_firewall_task(task):
    return 'ansible.posix.firewalld' in task or 'community.general.ufw' in task


def is_file_task(task):
    return 'file' in task or 'ansible.builtin.copy' in task \
           or 'copy' in task or 'lineinfile' in task or 'mount' in task or 'blockinfile' in task


# checks if a task installs a version-specific package
def check_task_for_version_specific_package(task):
    package_managers = ['apt', 'yum', 'dnf', 'pacman', 'apk', 'pip', 'snap']
    messages = []

    try:
        for t in task:
            for pm in package_managers:
                if pm in t:
                    if 'version' in task[t]:
                        messages.append(f"Task uses {pm} to install a specific version of a package.")
                    else:
                        messages.append(f"Task uses {pm} to install a latest version which could get incompatible.")
        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for version-specific packages:", str(e))
        return "Error"


def check_hardware_or_software_components(task, components, message):
    if any(component in task for component in components):
        return message
    return '\n'


def check_task_for_hardware_specific_commands(task):
    messages = []

    try:
        for t in task:
            for component in ['command', 'shell', 'raw']:
                if component in t:
                    messages.append(check_hardware_or_software_components(task[t], ['lspci', 'lshw'], "Task uses a hardware-specific command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['lsblk', 'fdisk', 'parted', 'mkfs', 'sg3_utils', 'multipath', 'disk_type', 'fstype'], "Task uses a disk management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['fwupd', 'smbios-util'], "Task uses a BIOS firmware management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['mdadm', 'megacli'], "Task uses a RAID arrays management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['tpmtool', 'efibootmgr'], "Task uses a security management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['cpufrequtils', 'sysctl', 'cpufreq-info', 'cpu_affinity'], "Task uses a performance settings management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['nvidia-settings', 'nvidia-smi'], "Task uses a GPU settings management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['xinput', 'xrandr'], "Task uses an I/O device management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(task[t], ['smbus-tools', 'lm-sensors'], "Task uses a system management bus command that may not be portable."))
                else:
                    messages.append(check_hardware_or_software_components(t, ['lspci', 'lshw'], "Task uses a hardware-specific command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['lsblk', 'fdisk', 'parted', 'mkfs', 'sg3_utils', 'multipath', 'disk_type', 'fstype'], "Task uses a disk management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['fwupd', 'smbios-util'], "Task uses a BIOS firmware management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['mdadm', 'megacli'], "Task uses a RAID arrays management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['tpmtool', 'efibootmgr'], "Task uses a security management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['cpufrequtils', 'sysctl', 'cpufreq-info', 'cpu_affinity'], "Task uses a performance settings management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['nvidia-settings', 'nvidia-smi'], "Task uses a GPU settings management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['xinput', 'xrandr'], "Task uses an I/O device management command that may not be portable."))
                    messages.append(check_hardware_or_software_components(t, ['smbus-tools', 'lm-sensors'], "Task uses a system management bus command that may not be portable."))
        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for hardware-specific commands:", str(e))
        return "Error"


def check_task_for_software_specific_commands(task):
    software_commands = ['npm', 'pip', 'docker', 'kubectl', 'ipblock',
                         'ip', 'ifconfig', 'route', 'vconfig', 'ifup', 'ifdown', 'iptables', 'k8s_cluster']
    messages = []

    try:
        for t in task:
            if 'command' in t or 'shell' in t or 'raw' in t:
                for command in software_commands:
                    if command in task[t]:
                        messages.append(f"Task uses a {command} command that may not be portable.")
                        break
            else:
                messages.append(check_hardware_or_software_components(t, software_commands, "task uses a software specific command."))
        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for software-specific commands:", str(e))
        return "Error"


def check_task_for_environment_assumptions(task):
    messages = []
    key_download_components = ['apt_repository', 'get_url', 'uri', 'apt_key', 'rpm_key', 'apt_get_key', 'yum_key',
                               'dnf_key', 'pacman_key', 'apk_key',
                               'ansible.builtin.rpm_key', 'ansible.builtin.apt_key',
                               'ansible.builtin.dnf_key', 'ansible.builtin.pacman_key', 'ansible.builtin.yum_key', 'url',
                               'git', 'remote_vars', 'repository', 'baseurl', 'gpgkey']
    try:
        for t in task:
            if has_environment_assumption(task, t):
                messages.append("Task assumes a default running environment.")

            if has_os_family_assumption(task, t):
                messages.append("Task assumes the operating system family.")

            if has_firewall_assumption(task, t):
                messages.append("Task assumes the firewall and changes the state without checking.")

            if has_dns_assumption(task, t):
                messages.append("Task assumes that the system is using a resolv.conf file to manage DNS settings.")

            if has_ethernet_assumption(task, t):
                messages.append("Task changes ethernet interfaces settings without checking the state.")

            if has_ntp_assumption(task, t):
                messages.append("Task assumes the system is using the ntp service to manage time settings and the provided NTP servers.")

            if has_ssh_assumption(task, t):
                messages.append("Task assumes that the system is using SSH without checking the state.")

            if has_package_repository_assumption(task, t, key_download_components):
                messages.append("Task assumes that the package repository is available at a specific URL structure.")

            if check_windows_command(t):
                messages.append("Task assume the environment is windows.")

        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for environment assumptions:", str(e))
        return "Error"


def check_windows_command(task_part):
    if 'windows.win' in task_part or 'win_' in task_part:
        return True


def has_environment_assumption(task, t):
    return ('vars' in t or 'include_vars' in t or 'include_tasks' in t or 'when' in t) and ('ansible_distribution' in str(task[t])) \
           or ('selinux' in t or 'ansible.windows.win_optional_feature' in t or 'ansible.windows.win_package' in t)


def has_os_family_assumption(task, t):
    return ('vars' in t or 'include_vars' in t or 'include_tasks' in t or 'when' in t) and ('ansible_os_family' in str(task[t])) \
           or ('selinux' in t or 'ansible.windows.win_optional_feature' in t or 'ansible.windows.win_package' in t)


def has_firewall_assumption(task, t):
    return ('ansible.posix.firewalld' in t or 'community.general.ufw' in t or 'firewall_rule' in t) and ('state' not in task[t])


def has_dns_assumption(task, t):
    return 'resolv.conf' in t and 'state' not in task[t]


def has_ethernet_assumption(task, t):
    return 'ethernets' in t and 'state' not in task[t]


def has_ntp_assumption(task, t):
    return 'ntp' in t and 'state' not in task[t]


def has_ssh_assumption(task, t):
    return 'sshd_config' in t and 'state' not in task[t]


def has_package_repository_assumption(task, t, key_download_components):
    return any(key_checker in str(t) for key_checker in key_download_components) \
           and ('url' in str(task[t]) or 'repo' in task[t] or 'repository' in task[t])


def check_task_for_missing_dependencies(task):
    messages = []

    try:
        for t in task:
            if 'msg' in t or 'failed_when' in t:
                if 'dependencies are missing' in task[t] or 'dependency not found' in task[t]:
                    messages.append("Task has missing dependencies")

            elif 'failed' in t and str(task[t]).lower() == 'false' or 'fail' in t:
                messages.append("Task has missing dependencies")

            elif 'file' in t or 'ansible.builtin.copy' in t or 'mount' in t:
                src_message = check_path(task, t, 'src', "Task is using absolute path for source", "Task is using relative path for source")
                path_message = check_path(task, t, 'path', "Task is using absolute path for source path", "Task is using relative path for source path")
                messages.append(src_message)
                messages.append(path_message)

        if messages:
            return '\n'.join(messages)
        else:
            return "None"

    except Exception as e:
        print("Error occurred while checking task for missing dependencies:", str(e))
        return "Error"


def check_path(task, t, key, absolute_message, relative_message):
    from pathlib import Path
    message = ''
    if key in task[t]:
        dest = task[t][key]
        if Path(str(dest)).is_absolute():
            message = absolute_message
        else:
            message = relative_message
    return message


def get_task_name(task, task_index):
    try:
        task_name = task['name']
    except KeyError:
        task_name = 'Task ' + str(task_index)
    except Exception as e:
        print("Error occurred while getting task name:", str(e))
        task_name = 'Task ' + str(task_index)
    return task_name


def get_tasks_line_numbers(input_file):
    try:
        task_line_numbers = []
        line_number = 0
        # Open the file and get the task line numbers
        with open(input_file) as file:
            for line in file:
                line_number += 1
                line = line.strip()
                if line.startswith('-'):
                    task_line_numbers.append(line_number)
        return task_line_numbers
    except FileNotFoundError:
        print("File not found:", input_file)
        return []
    except IOError as e:
        print("I/O error occurred while reading the file:", str(e))
        return []
    except Exception as e:
        print("An error occurred:", str(e))
        return []


def create_task_smells(task_name, smell_name_description):
    task_smells = {
        'Task name': task_name,
        'Idempotency': smell_name_description['Idempotency'],
        'Version specific installation': smell_name_description['Version Specific Installation'],
        'Outdated dependencies': smell_name_description['Outdated Dependencies'],
        'Missing dependencies': smell_name_description['Missing Dependencies'],
        'Assumption about environment': smell_name_description['Assumption about Environment'],
        'Hardware specific commands': smell_name_description['Hardware Specific Commands'],
        'Broken Dependency': smell_name_description['Broken Dependency Chain']
    }
    return task_smells


def detect_smells(task, task_number, input_file):
    try:
        output_tasks = []
        new_output_tasks = []

        # Extract file name and repository name for output
        file_name = os.path.basename(input_file)
        repository_name = os.path.dirname(input_file)

        # Get task line numbers
        task_line_numbers = get_tasks_line_numbers(input_file)

        smell_name_description = perform_smell_detection_for_task(task=task)
        task_name = get_task_name(task=task, task_index=task_number)

        # Store task smells in a dictionary
        task_smells = create_task_smells(task_name, smell_name_description)
        output_tasks.append(task_smells)

        for smell_name, smell_description in smell_name_description.items():
            new_task_smells = {
                'Repository Name': repository_name,
                'File Name': file_name,
                'Line Number': task_line_numbers[task_number-1],
                'Task Name': task_name,
                'Smell Name': smell_name,
                'Smell Description': smell_description,
            }
            new_output_tasks.append(new_task_smells)

        return output_tasks, new_output_tasks
    except IndexError:
        print("Task number is out of range.")
    except Exception as e:
        print("An error occurred:", str(e))

    return [], []


def perform_smell_detection_for_task(task):
    smell_name_description = {}

    try:
        smell_name_description['Idempotency'] = check_task_for_idempotency(task=task)
        smell_name_description['Version Specific Installation'] = check_task_for_version_specific_package(task=task)
        smell_name_description['Outdated Dependencies'] = check_task_for_outdated_package(task=task)
        smell_name_description['Missing Dependencies'] = check_task_for_missing_dependencies(task=task)
        smell_name_description['Hardware Specific Commands'] = check_task_for_hardware_specific_commands(task=task)
        assumption = check_task_for_environment_assumptions(task=task) + ' ' + check_task_for_software_specific_commands(task=task)
        smell_name_description['Assumption about Environment'] = assumption
        smell_name_description['Broken Dependency Chain'] = check_task_for_broken_dependency(task=task)
    except Exception as e:
        print("An error occurred during smell detection:", str(e))

    return smell_name_description