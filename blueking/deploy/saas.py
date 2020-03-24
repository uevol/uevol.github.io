#!/bin/python3
# -*- coding: utf-8 -*-
# @filename saas.py
# @author WillYang
# @email WillYang@canway.net
# @description deploy bk saas. adapted based on install/saas.py
# @created 2020-03-24T10:40:15.303Z+08:00
# @last-modified 2020-03-24T17:25:01.994Z+08:00

import argparse
import logging
import os
import sys
import time

import pymysql
import requests
import urllib3

urllib3.disable_warnings()

HTTP_SCHEMA = os.environ.get("HTTP_SCHEMA", "http")


class AppManager(object):

    def __init__(self, paas_domain, environment=None):
        self.paas_domain = paas_domain

        if environment is not None:
            self.env = environment

        self.session = requests.Session()
        self.session.headers.update({'referer': "%s://%s" % (HTTP_SCHEMA, paas_domain)})
        self.session.verify = False

    def get_csrftoken(self, url, token_name):
        resp = self.session.get(url, verify=False)
        if resp.status_code == 200:
            logg.info(resp.cookies)
            return resp.cookies[token_name]

        logg.error("get token({}) failed. http code:{}".format(token_name, resp.status_code))
        sys.exit(1)

    def login(self, login_url, username, passwd):
        self.username = username
        self.passwd = passwd

        logg.info("request login token")
        login_csrftoken = self.get_csrftoken(login_url, 'bklogin_csrftoken')

        login_form = {
            'csrfmiddlewaretoken': login_csrftoken,
            'username': username,
            'password': passwd
        }

        logg.info("emulate login to {}, form data: {}".format(login_url, login_form))
        resp = self.session.post(login_url, data=login_form, verify=False)

        if resp.status_code == 200:
            logg.info("bklogin_csrftoken: {}".format(resp.cookies.get("bklogin_csrftoken")))
            return resp.cookies

        logg.error("login failed.")
        sys.exit(1)

    def simple_check(self, url):
        resp = self.session.get(url)
        assert resp.status_code == 200

    def set_env(self, env_name):
        self.env = env_name

    def set_appcode(self, app_code):
        self.app_code = app_code

    def add_broker(self, broker_protocol, broker_url, broker_user, broker_pass):
        self.broker_url = broker_url

    def upload_pkg(self, file_path, token_url, upload_url=None):
        logg.info("request bk_csrftoken")
        upload_csrftoken = self.get_csrftoken(token_url, 'bk_csrftoken')
        logg.info("get upload token:{} from {}".format(upload_csrftoken, token_url))

        if upload_csrftoken is None:
            logg.info("upload package failed")
            sys.exit(1)

        if upload_url is None:
            upload_url = token_url.replace("/release", "")

        files = {'saas_file': open(file_path, 'rb')}
        token = {'csrfmiddlewaretoken': upload_csrftoken}

        logg.info("uploading file {}, url:{}, data: {} ...".format(file_path, upload_url, token))
        resp = self.session.post(upload_url, files=files, data=token)

        if resp.status_code != 200:
            logg.error("upload faild:{}".format(resp.content))
            sys.exit(1)

        if "danger" in resp.text:
            logg.info("upload package failed!: {}".format(resp.text.encode('utf-8')))
            sys.exit(1)

    def deploy(self, url, env):

        env_data = {"mode": env}

        logg.info("start deploy {}, upload_csrftoken: {} ".format(app_code, self.session.cookies.get("bk_csrftoken")))
        resp = self.session.post(
                url=url,
                data=env_data,
                headers={"X-CSRFToken": self.session.cookies.get("bk_csrftoken")}
            )

        if resp.status_code != 200:
            logg.error("request deploy api failed: {}".format(resp.content))
            sys.exit(1)

        logg.info(u"  resposne: {}".format(resp.json()))
        deploy_result = resp.json()
        if deploy_result['result'] is False:
            logg.info(u"{}".format(deploy_result["msg"]))
            sys.exit(1)

        return deploy_result["event_id"], deploy_result["app_code"]

    def check_result(self, url, app_code, event_id, timeout):
        for i in range(timeout):
            time.sleep(2)
            logg.info(" check deploy result. retry {}".format(i))
            resp = self.session.get("{}{}/?event_id={}".format(url, app_code, event_id))
            if resp.json()["result"]:
                if resp.json()["data"]["status"] == 2:
                    logg.debug("  check result: {}".format(resp.json()))
                elif resp.json()["data"]["status"] == 1:
                    logg.info("{} have been deployed successfully".format(app_code))
                    return resp.json
                else:
                    logg.error("\x1b[31;40mdeploy failed: timeout\x1b[0m")
                    sys.exit(1)


class SimpleDB(object):
    def __init__(self, **kwargs):
        self.dbc = pymysql.connect(**kwargs)

    def close(self):
        self.dbc.close()

    def execute(self, sql):
        cursor = self.dbc.cursor()
        cursor.execute(sql)

        rec = cursor.fetchone()
        if rec:
            return rec[0]
        else:
            return None

    def __del__(self):
        self.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='deploy blueking saas by script')
    p.add_argument('-e', required=True, dest='deploy_env', help=u'部署环境')
    p.add_argument('-n', required=True, dest='app_code', help=u'蓝鲸SAAS的app code')
    p.add_argument('-k', required=True, dest='pkg_path', help=u'部署包所在路径')
    p.add_argument('-f', required=True, dest='paas_fqdn', help=u'平台域名')
    p.add_argument('-p', required=True, dest='paas_https_port', default='80', help=u'平台web端口')
    p.add_argument('-u', required=True, dest='paas_admin_user', default='admin', help=u'部署时使用账号')
    p.add_argument('-P', required=True, dest='paas_admin_pass', help=u'部署账号密码')
    p.add_argument('-b', required=True, dest='mysql_host', help=u'平台SAAS使用mysql主机')
    p.add_argument('-a', required=True, dest='mysql_user', help=u'mysql用户')
    p.add_argument('-s', required=True, dest='mysql_pass', help=u'mysql用户密码')
    p.add_argument('-m', required=True, dest='mysql_port', help=u'mysql端口')
    p.add_argument('-d', dest='debug_enable', choices=('debug_enable',), help='debug mode')
    args = p.parse_args()

    saas_env = {
            'appt': 'test',
            'appo': 'prod'
        }

    if args.debug_enable:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    paas_domain = '{}:{}'.format(args.paas_fqdn, args.paas_https_port)
    username = args.paas_admin_user
    password = args.paas_admin_pass
    pkg_path = args.pkg_path
    app_code = args.app_code

    # 日志配置
    log_fmt = "%(asctime)s %(lineno)-4s %(levelname)-6s %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(log_fmt)
    logging.basicConfig(format=log_fmt, datefmt=date_fmt, level=log_level)

    # 检查日志文件是否存在
    if not os.path.exists('logs/'):
        os.mkdir('logs/')
        if not os.path.exists('./logs/deploy_saas.log'):
            os.system('touch ./logs/deploy_saas.log')

    fh = logging.FileHandler("./logs/deploy_saas.log")
    fh.setFormatter(formatter)

    logg = logging.getLogger()
    logg.addHandler(fh)

    # DB 信息
    db_config = {
            "host": args.mysql_host,
            "user": args.mysql_user,
            "passwd": args.mysql_pass,
            "port": int(args.mysql_port),
            "db": 'open_paas'
        }

    x = SimpleDB(**db_config)
    checknew_sql = "select id from open_paas.paas_saas_app where code='{}'".format(app_code)
    if not x.execute(checknew_sql):
        # 首次上传, 设置 app_code 为0
        app_code = "0"

    # 各步骤 url 设置
    login_url = "{}://{}/login/".format(HTTP_SCHEMA, paas_domain)
    check_app_url = "{}://{}/app/list/".format(HTTP_SCHEMA, paas_domain)

    upload_token_url = "{}://{}/saas/upload/{}/".format(HTTP_SCHEMA, paas_domain, app_code)
    upload_url = "{}://{}/saas/upload/{}/".format(HTTP_SCHEMA, paas_domain, app_code)

    # main progress
    appmgr = AppManager(paas_domain)
    appmgr.login(login_url, username, password)
    appmgr.simple_check(check_app_url)
    appmgr.upload_pkg(pkg_path, upload_token_url, upload_url)

    event_id_SQL = """
        SELECT a.id FROM paas_saas_app_version a, paas_saas_app b, paas_saas_upload_file c
        WHERE code='{}' and a.saas_app_id = b.id and a.upload_file_id = c.id
        ORDER BY c.id desc limit 1
    """.format(app_code)

    x = SimpleDB(**db_config)
    saas_version_id = x.execute(event_id_SQL)

    logg.info("query saas_version_id: {}".format(saas_version_id))

    deploy_url = "{}://{}/saas/release/online/{}/".format(HTTP_SCHEMA, paas_domain, saas_version_id)
    logg.info("start deploy app:{} url: {}".format(args.app_code, deploy_url))
    event_id, app_code = appmgr.deploy(deploy_url, saas_env[args.deploy_env])

    check_event_url = "{}://{}/release/get_app_poll_task/".format(HTTP_SCHEMA, paas_domain)
    logg.info("checking deploy result...")
    appmgr.check_result(check_event_url, app_code, event_id, 600)
