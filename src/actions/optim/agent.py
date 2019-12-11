import os,time,sys

class agent():
    def openDB(self):
        sys.path.append('C:\\Python27')
        sys.path.append('C:\\Python27\\Lib\\site-packages')
        import pymysql as mysqldb
        conn = None
        try:
            conn = mysqldb.connect(host="10.206.1.21", user="root", passwd="actiontec123", port=3306, connect_timeout=60)
            conn.select_db("optim")
        except Exception, e:
            print e
            print 'open db failed'
        return conn


    def exec_SQL(self,sql):
        conn = self.openDB()
        r = False
        result_set = None
        if conn:
            try:
                cursor = conn.cursor()
                r = cursor.execute(sql)
                conn.commit()
                result_set = cursor.fetchall()
                cursor.close()
                conn.close()
            except Exception, e:
                print "exec_SQL fail"
        else:
            pass
        return (r, result_set)

    def raiseError(Message=None):
        raise Exception,Message
        
    def log(self,params):
        s=params['message']
        print s
    
    def getCustomEnvValue(self,params):
        key=params['key']
        sql="select * from optim_web_element_location_%s" %(os.getenv('Optim_Web_Server_Version'))
        print sql
        r,result_set=self.exec_SQL(sql)
        print result_set
        for item in result_set:
            cur_name=item[1]
            cur_value=item[2]
            if cur_name.lower()==key.lower():
                print item
                return cur_value
        raiseError(Message="ERROR : Not Find element web location value!")
        
    def selectwebdriver(self,params):
        browser=params['webbrowser']
        if browser.lower()=='firefox':
            print 'Info : Browser if Firefox.'
            return True
        p=os.popen('C:\\tmp\\killchromedriver.cmd')
        print p.read()
        
        ver=params['version']
        exefiles="C:\\Program Files (x86)\\RedwoodHQ Agent\\agent\\executionfiles"
        laestfile=None
        laesttime=0
        for pth in os.listdir(exefiles):
            curfile=os.path.join(exefiles,pth)
            if os.path.isdir(curfile):
                curt=os.path.getmtime(curfile)
                if curt > laesttime:
                    laesttime=curt
                    laestfile=curfile
            else:
                continue
        if browser.lower()=='chrome':
            cmd='copy "%s\\bin\\chromedriver.exe.%s" "%s\\bin\\chromedriver.exe" /y' %(laestfile,ver,laestfile)
            print cmd
            rc=os.system(cmd)
            print rc
            if rc==1:
                print "Error : chromedriver copy fail!"
            time.sleep(2)
        
    def report(self,params):
        sys.path.append('C:\\Python27')
        sys.path.append('C:\\Python27\\Lib\\site-packages')
        sys.path.append("C:\\Program Files (x86)\\RedwoodHQ Agent\\agent\\executionfiles")
        from AgentSimulator import AgentSimulator
        repeat=params['repeat']
        para=params['para']
        sn=params['sn']
        mqtt = AgentSimulator()
        rc = mqtt.send_mqtt_packet(sn, node_para=[para],repeat=int(repeat))
        print rc
        time.sleep(60)
