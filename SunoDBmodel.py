class Session():
    def __init__ (self, session_id, session_name, scen_version, sess_beg, sess_end,sess_dur, sess_status, sess_mess , agent_name, context_code, status ):
        self.session_id=session_id
        self.session_name=session_name
        self.scen_version=scen_version
        self.sess_beg=sess_beg
        self.sess_end=sess_end
        self.sess_dur=sess_dur
        self.sess_status=sess_status
        self.sess_mess=sess_mess
        self.agent_name=agent_name
        self.context_code=context_code
        self.status = status

class SessTasks():
    def __init__(self, session_id, nno, scen_task_no,task_type, task_name1,task_name2, task_name3, exe_channel,def_context_code,  \
                    def_lschema_name, def_con_name, col_lschema_name, col_con_name, begine_time, end_time, task_duration, task_status, \
                    task_mess, nb_row, nb_ins, nb_upd, nb_del, nb_err, status ):
        self.session_id=session_id
        self.nno=nno
        self.scen_task_no=scen_task_no
        self.task_type=task_type
        self.task_name1=task_name1
        self.task_name2=task_name2
        self.task_name3=task_name3
        self.exe_channel=exe_channel
        self.def_context_code=def_context_code
        self.def_lschema_name=def_lschema_name
        self.def_con_name=def_con_name
        self.col_lschema_name=col_lschema_name
        self.col_con_name=col_con_name
        self.begine_time=begine_time
        self.end_time=end_time
        self.task_duration=task_duration
        self.task_status=task_status
        self.task_mess=task_mess
        self.nb_row=nb_row
        self.nb_ins=nb_ins
        self.nb_upd=nb_upd
        self.nb_del=nb_del
        self.nb_err=nb_err
        self.status=status

class Step():
    def __init__(self, session_id, nno,nb_run,step_name,step_type,context_code,task_beg,task_end,task_status, task_dur,task_rc, \
                    task_mess,nb_row,nb_ins,nb_upd,nb_del,nb_err,status):
        self.session_id = session_id
        self.nno=nno
        self.nb_run=nb_run
        self.step_name=step_name
        self.step_type=step_type
        self.context_code=context_code
        self.task_beg=task_beg
        self.task_end=task_end
        self.task_dur=task_dur
        self.task_status=task_status
        self.task_rc=task_rc
        self.task_mess=task_mess
        self.nb_row=nb_row
        self.nb_ins=nb_ins
        self.nb_upd=nb_upd
        self.nb_del=nb_del
        self.nb_err=nb_err
        self.status=status
