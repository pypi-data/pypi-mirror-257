# -*- encoding: utf-8 -*-
'''
@File		:	matter_command.py
@Time		:	2024/01/05 10:26:11
@Author		:	dan
@Description:	matter 命令行入口

matter proxy -p [port]    
开启代理服务器，监听来自远端测试脚本的命令


'''

import argparse
import matter.command.run_proxy as run_proxy
import matter.command.record as record
import matter.command.run as run


def run(args):
    parser = argparse.ArgumentParser("matter", add_help=False)
    parser.add_argument('run_proxy', help="开启代理服务器", action="store_false")
    parser.add_argument('run', help="运行 matter 测试用例", action="store_false")
    parser.add_argument('record', help="运行录制管理器", action="store_false")
    parser.add_argument('-h', help='查看帮助', required=False, action="store_false")
    parser.print_help()
    # parser.print_help()
    result, unknown = parser.parse_known_args()

    if result.h:
        parser.print_help()
        return;

    if result.run_proxy:
        # run_proxy_parser = argparse.ArgumentParser("matter run_proxy", description="运行代理", add_help=False)
        # run_proxy_parser.add_argument('-p', '--port', help='指定监听端口端口', type=int)
        # run_proxy_parser.add_argument('-h', help='查看帮助')
        # run_proxy_parser.parse_args(args[2:-1])
        return run_proxy.run(args[2:-1])

    if result.record:
        # run_proxy_parser = argparse.ArgumentParser("matter run_proxy", description="运行代理", add_help=False)
        # run_proxy_parser.add_argument('-p', '--port', help='指定监听端口端口', type=int)
        # run_proxy_parser.add_argument('-h', help='查看帮助')
        # run_proxy_parser.parse_args(args[2:-1])
        return record.run(args[2:-1])

    parser.print_help()


if __name__ == '__main__':
    import sys
    try:
        args = sys.argv;
        args.append("run_proxy")
        args.append("-h")
        run(args)
    except Exception as e:
        print(e)