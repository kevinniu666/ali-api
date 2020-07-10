#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt,slb,myemail,os
def main(argv):
   orig_master_host = ''
   new_master_host = ''
   new_slave_hosts=''
   email_subject=''
   email_body=''
   conf=''
   try:
      opts, args = getopt.getopt(argv,"ho:n:s:S:b:c:",["orig_master_host=","new_master_host=","new_slave_hosts=","subject=","body=","conf="])
   except getopt.GetoptError as e:
      print "send_report.py --orig_master_host=<dead master's hostname> --new_master_host=<new master's hostname> --new_slave_hosts=<new slaves' hostnames, delimited by commas> --subject=(mail subject) --body=(body) --conf=(mha config file)"
      print e
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print "send_report.py --orig_master_host=<dead master's hostname> --new_master_host=<new master's hostname> --new_slave_hosts=<new slaves' hostnames, delimited by commas> --subject=(mail subject) --body=(body) --conf=(mha config file)"
         sys.exit()
      elif opt in ("-o", "--orig_master_host"):
         orig_master_host = arg
      elif opt in ("-n", "--new_master_host"):
         new_master_host = arg
      elif opt in ("-s", "--new_slave_hosts"):
         new_slave_hosts = arg
      elif opt in ("-S", "--subject"):
         email_subject = arg
      elif opt in ("-b", "--body"):
         email_body = arg
      elif opt in ("-c", "--conf"):
         conf = arg
   print '原来的master地址为：', orig_master_host
   print '新的master地址为：', new_master_host
   print '新的slave地址为: ', new_slave_hosts
   print 'email subject 为: ', email_subject
   print 'email body 为: ', email_body
   #切换阿里云的SLB后端服务组
   NewBackendServers = ''
   OldBackendServers = ''
   # new_master_host = '10.128.146.185'
   if new_master_host == '172.16.3.122':
      OldBackendServers = '[{ "ServerId": "i-wz949h0dw8516dvkwd2o",' \
                          '"Weight": "100",' \
                          '"Type": "ecs",' \
                          '"Port":"3306"}]'
      NewBackendServers = '[{ "ServerId": "i-wz96dai3e434sqzii3tb",' \
                          '"Weight": "100",' \
                          '"Type": "ecs",' \
                          '"Port":"3306"}]'
   elif new_master_host == '172.16.2.196':
      OldBackendServers = '[{ "ServerId": "i-wz96dai3e434sqzii3tb",' \
                          '"Weight": "100",' \
                          '"Type": "ecs",' \
                          '"Port":"3306"}]'
      NewBackendServers = '[{ "ServerId": "i-wz949h0dw8516dvkwd2o",' \
                          '"Weight": "100",' \
                          '"Type": "ecs",' \
                          '"Port":"3306"}]'
   slb.modify_VServerGroupBackendServers(OldBackendServers, NewBackendServers)
   #发送邮件给运维人员
   current_path = os.path.abspath('.')
   # attachment = os.path.join(current_path, 'pie.xlsx')
   receiver = ['12345678@qq.com'] #告警邮件接收人
   subject = email_subject
   body = email_body
   myemail.mail(receiver, subject, body)
if __name__ == "__main__":
   for item in sys.argv:
       print item
   main(sys.argv[1:])
