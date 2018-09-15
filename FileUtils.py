from pexpect import pxssh
from pprint import pprint

def checkFileExists(server, uname, passwd, file):
    s = pxssh.pxssh()
    s.login(server, uname, passwd)
    s.sendline('file  %s' % file)  # run a command
    s.prompt()  # match the prompt
    content = s.before
    return content


# pprint(checkFileExists("aquila-ext-15.pluribusnetworks.com", "root", "test123",
#                        "/nvOS/export/restExport-33.tar.gz.2016-01-10T22.23.12.tar.gz"))
