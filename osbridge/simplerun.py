from subprocess import PIPE, Popen
from sys import argv, stdout as sys_stdout, stderr as sys_stderr
from shlex import split


cmd = split(' '.join(argv[1:]))

proc = Popen(cmd, stdout=PIPE)
stdout, stderr = proc.communicate()
print >> sys_stdout, stdout,
if stderr:
    print >> sys_stderr, stderr,

exit(proc.returncode)
