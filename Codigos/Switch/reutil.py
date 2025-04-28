
"""
Habilitando Advanced CLI em switches modelo:
- HP 1910
- HP 1920
- HP 1950
Habilitando o screen-length 0 em switches modelo:
- 3Com S4210 26-Port
- 3Com S4500-26
Salvando configuracao em switches Comware 5 e Comware 7
"""

# 1910 - habilitar advanced CLI
def login_1910(net_connect):
    output = net_connect.send_command_timing("_cmdline-mode on")
    if "[Y/N]" in output:
        output += net_connect.send_command_timing("y")
    if "Please input password:" in output:
        output += net_connect.send_command_timing("512900")
    net_connect.send_command_timing("screen-lenght disable")
    net_connect.send_command_timing("undo terminal monitor")

# 1920 - habilitar advanced CLI
def login_1920(net_connect):
    output = net_connect.send_command_timing("_cmdline-mode on")
    if "[Y/N]" in output:
        output += net_connect.send_command_timing("y")
    if "Please input password:" in output:
        output += net_connect.send_command_timing("Jinhua1920unauthorized")
    net_connect.send_command_timing("screen-lenght disable")
    net_connect.send_command_timing("undo terminal monitor")

# 1950 - habilitar advanced CLI
def login_1950(net_connect):
    output = net_connect.send_command_timing("xtd-cli-mode")
    if "[Y/N]" in output:
        output += net_connect.send_command_timing("y")
    if "Password:" in output:
        output += net_connect.send_command_timing("foes-bent-pile-atom-ship")
    net_connect.send_command_timing("undo terminal monitor")

# 4210/4500 - desabilitar screen-length
def screen_leng_4210_4500(net_connect):
    commands_screen_leng = ['user-interface vty 0 4',
        'screen-length 0',
        'quit', 'quit']
    net_connect.send_config_set(commands_screen_leng)
    net_connect.send_command_timing("undo terminal monitor")

# configurar senha aruba 2530/2430/2930
def pass_aruba(net_connect):
    output = net_connect.send_command_timing("password operator")
    if "New password for operator:" in output:
        output += net_connect.send_command_timing("==senha==")
    if "Re-enter the new password for operator:" in output:
        output += net_connect.send_command_timing("==senha==")
    output = net_connect.send_command_timing("password manager user-name admin")
    if "New password for manager:" in output:
        output += net_connect.send_command_timing("==senha==")
    if "Re-enter the new password for manager:" in output:
        output += net_connect.send_command_timing("==senha==")


#save Comware 5 e Comware 7
def comware_save(net_connect):
    command_comware_save = ['sa sa',
        'Y',
        '',
        'Y',
        ]
    net_connect.send_config_set(command_comware_save, read_timeout=150)
