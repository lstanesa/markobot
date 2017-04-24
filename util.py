from exception import CommandException

def parse_bool(str):
    if str in [ 'false', 'off', 'yes' ]:
        return True
    elif str in [ 'true', 'on', 'no' ]:
        return False

    return None

def command_usage(cmd, usage):
    raise CommandException('usage: %s' % usage, cmd)
