import cx_Oracle
from SunoDBmodel import Session, SessTasks, Step


class OracleSession:

    def __init__(self, user, passw, db):
        try:
            self.con = cx_Oracle.connect(user, passw, db)
            self.cur = self.con.cursor()
        except cx_Oracle.DatabaseError as e:
            return( "Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
    def __exit__(self):
        self.disconnect()
    def connect(self,user, passw, db):
        pass

    def disconnect(self):
        try:
            self.cur.close()
            self.con.close()
        except cx_Oracle.DatabaseError:
            pass
    def get_sessions(self):
        sessions =[]

        self.cur.execute("select sess_no, sess_name, scen_version,sess_beg, sess_end, trunc(sess_dur),\
                                            sess_status, sess_mess, agent_name, context_code \
                        from snp_session where sess_beg>sysdate-1 \
                        order by sess_beg desc")
        res =self.cur.fetchall()
        for line in res:
            sts = self.resolve_status(line[6])

            sessions.append(Session(line[0], line[1],line[2],line[3],line[4],line[5],line[6], line[7], line[8],line[9], sts ))
            #print(sessions[0].session_id)
        return sessions
    def get_failed_sessions(self, siteno, items_per_site):
        failed = []

        if self.get_sessions_count('E') < (siteno * items_per_site):
            print(self.get_sessions_count('E') )
            return False
        else:
            beg = items_per_site * siteno - items_per_site

            end = items_per_site * siteno

            sql = (f"select * from \
                             (select a.* , rownum rnum from \
                                    (select sess_no, sess_name, scen_version,sess_beg, sess_end, trunc(sess_dur),\
                                            sess_status, sess_mess, agent_name, context_code \
                                            from snp_session order by sess_beg desc) a \
                                            where 1=1 \
                                                and sess_status='E' \
                                                and rownum <= {end} )\
                                    where rnum >= {beg}")


            self.cur.execute(sql)
            res = self.cur.fetchall()
            for line in res:
                sts = self.resolve_status(line[6])
                failed.append(Session(line[0], line[1],line[2],line[3],line[4],line[5],line[6], line[7], line[8], line[9], sts))

            return failed

    def get_session_page(self, siteno, items_per_site):
        sessions = []
        if self.get_sessions_count() < (siteno*items_per_site):
            #print(self.get_sessions_count() )
            return False
        else:
            beg = items_per_site * siteno - items_per_site
            end = items_per_site * siteno
            sql = (f"select * from \
                                (select a.* , rownum rnum from \
                                    (select sess_no, sess_name, scen_version,sess_beg, sess_end, trunc(sess_dur),\
                                            sess_status, sess_mess, agent_name, context_code \
                                    from snp_session order by sess_beg desc) a \
                                    where rownum <= {end} )\
                            where rnum >= {beg}")

            self.cur.execute(sql)
            res = self.cur.fetchall()
            for line in res:
                sts = self.resolve_status(line[6])
                sessions.append(Session(line[0], line[1],line[2],line[3],line[4],line[5],line[6], line[7], line[8],line[9], sts ))
            return sessions

    def get_session(self, session_id):

        sql= (f"select sess_no, sess_name, scen_version,sess_beg, sess_end, trunc(sess_dur),\
                                            sess_status, sess_mess, agent_name, context_code \
                                    from snp_session \
                                     where sess_no={session_id}")
        self.cur.execute(sql)
        res = self.cur.fetchone()
        sts = self.resolve_status(res[6])

        session=Session(res[0], res[1],res[2],res[3],res[4],res[5],res[6], res[7], res[8],res[9], sts )
        return session

    def get_session_steps(self, session_id):
        session_steps=[]
        sql=f"select st.sess_no, st.nno, st.nb_run, st.step_name, st.step_type, st.context_code, \
                    sl.step_beg, sl.step_end, sl.step_dur, sl.step_status, sl.step_rc, sl.step_mess, \
                    sl.nb_row, sl.nb_ins, sl.nb_upd, sl.nb_del, sl.NB_ERR \
                    from SNPP.SNP_SESS_step st, SNPP.SNP_STEP_LOG sl \
                    where 1=1 \
                    and sl.SESS_NO(+) = ST.SESS_NO \
                    and sl.NB_RUN(+) = ST.NB_RUN \
                    and sl.NNO(+) = ST.NNO \
                    and  st.sess_no={session_id}  \
                        order by st.nno asc"

        self.cur.execute(sql)
        res = self.cur.fetchall()
        for line in res:
            sts = self.resolve_status(line[9], line[2] )
            session_steps.append(Step(line[0],line[1], line[2],  line[3], line[4], line[5], line[6], line[7] , line[8], line[9], \
                                           line[10], line[11], line[12], line[13], line[14], line[15], line[16], sts))
        return session_steps



    def get_session_step_tasks(self, session_id):
        session_step_tasks =[]
        sql=f"select st.sess_no,st.NNO, st.SCEN_TASK_NO, ST.TASK_TYPE, ST.TASK_NAME1, ST.TASK_NAME2, ST.TASK_NAME3, \
                st.EXE_CHANNEL , ST.DEF_CONTEXT_CODE, ST.DEF_LSCHEMA_NAME, ST.DEF_CON_NAME, st.COL_LSCHEMA_NAME,  \
                st.COL_CON_NAME, stl.TASK_BEG , stl.TASK_END, stl.TASK_DUR, stl.TASK_STATUS, stl.TASK_MESS, \
                stl.NB_ROW, stl.NB_INS, stl.NB_UPD, stl.NB_DEL, stl.NB_ERR   \
                from snpp.snp_sess_task st, SNPP.SNP_SESS_TASK_LOG stl  \
                where 1=1 \
                and STL.SESS_NO = ST.SESS_NO\
                and STL.NNO = ST.NNO\
                and STL.SCEN_TASK_NO = ST.SCEN_TASK_NO\
                and st.sess_no={session_id} "

        self.cur.execute(sql)
        res = self.cur.fetchall()

        for line in res:
            sts =self.resolve_status(line[16])


            session_step_tasks.append(SessTasks(line[0],line[1], line[2],  line[3], line[4], line[5], line[6], line[7] , line[8], line[9], \
                                           line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], \
                                           line[20], line[21], line[22] , sts))
        return session_step_tasks

    def get_log_txt(self, session_id, scen_task_no):
        log_text=''
        sql=f"select txt from SNPP.SNP_SESS_TXT_LOG \
                where sess_no={session_id} and scen_task_no={scen_task_no} \
                order by txt_ord asc"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for line in res:
            log_text += line[0]
        return log_text


    def get_sessions_count(self, type='ALL'):
        sql="select count(sess_no) from snp_session "
        if type != 'ALL':
            sql= sql + f" where sess_status='{type}'"
        self.cur.execute(sql)
        res = self.cur.fetchone()
        return res[0]

    def get_nof_sites(self,items_per_page, type='ALL'):
        return round(self.get_sessions_count(type)/items_per_page)

    def resolve_status(self, sts, run=1):
        if run==1:
            if sts == "E":
                return 'danger'
            elif sts == "R":
                return 'primary'
            elif sts == "M":
                return 'warning'
            else:
                return 'success'
        else:
            return 'secondary'