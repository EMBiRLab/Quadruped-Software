import lcm
import numpy as np
import sys
import random
import csv
import time
sys.path.append('../')
sys.path.append('./lcm-types/python/')
from leg_control_command_lcmt import leg_control_command_lcmt
from leg_control_data_lcmt import leg_control_data_lcmt
from state_estimator_lcmt import state_estimator_lcmt
from mpc_state_data_t import mpc_state_data_t

class Handler:

    def __init__(self):
        self.buffer = [0 for x in range(305)]
        self.header = ['time','cmd_tau_ff_0','cmd_tau_ff_1','cmd_tau_ff_2','cmd_tau_ff_3','cmd_tau_ff_4','cmd_tau_ff_5','cmd_tau_ff_6','cmd_tau_ff_7','cmd_tau_ff_8','cmd_tau_ff_9','cmd_tau_ff_10','cmd_tau_ff_11',
                'cmd_f_ff_0','cmd_f_ff_1','cmd_f_ff_2','cmd_f_ff_3','cmd_f_ff_4','cmd_f_ff_5','cmd_f_ff_6','cmd_f_ff_7','cmd_f_ff_8','cmd_f_ff_9','cmd_f_ff_10','cmd_f_ff_11',
                'cmd_q_des_0','cmd_q_des_1','cmd_q_des_2','cmd_q_des_3','cmd_q_des_4','cmd_q_des_5','cmd_q_des_6','cmd_q_des_7','cmd_q_des_8','cmd_q_des_9','cmd_q_des_10','cmd_q_des_11',
                'cmd_qd_des_0','cmd_qd_des_1','cmd_qd_des_2','cmd_qd_des_3','cmd_qd_des_4','cmd_qd_des_5','cmd_qd_des_6','cmd_qd_des_7','cmd_qd_des_8','cmd_qd_des_9','cmd_qd_des_10','cmd_qd_des_11',
                'cmd_p_des_0','cmd_p_des_1','cmd_p_des_2','cmd_p_des_3','cmd_p_des_4','cmd_p_des_5','cmd_p_des_6','cmd_p_des_7','cmd_p_des_8','cmd_p_des_9','cmd_p_des_10','cmd_p_des_11',
                'cmd_v_des_0','cmd_v_des_1','cmd_v_des_2','cmd_v_des_3','cmd_v_des_4','cmd_v_des_5','cmd_v_des_6','cmd_v_des_7','cmd_v_des_8','cmd_v_des_9','cmd_v_des_10','cmd_v_des_11',
                'kp_cartesian_0','kp_cartesian_1','kp_cartesian_2','kp_cartesian_3','kp_cartesian_4','kp_cartesian_5','kp_cartesian_6','kp_cartesian_7','kp_cartesian_8','kp_cartesian_9','kp_cartesian_10','kp_cartesian_11',
                'kd_cartesian_0','kd_cartesian_1','kd_cartesian_2','kd_cartesian_3','kd_cartesian_4','kd_cartesian_5','kd_cartesian_6','kd_cartesian_7','kd_cartesian_8','kd_cartesian_9','kd_cartesian_10','kd_cartesian_11',
                'kp_joint_0','kp_joint_1','kp_joint_2','kp_joint_3','kp_joint_4','kp_joint_5','kp_joint_6','kp_joint_7','kp_joint_8','kp_joint_9','kp_joint_10','kp_joint_11',
                'kd_joint_0','kd_joint_1','kd_joint_2','kd_joint_3','kd_joint_4','kd_joint_5','kd_joint_6','kd_joint_7','kd_joint_8','kd_joint_9','kd_joint_10','kd_joint_11',
                'data_q_0','data_q_1','data_q_2','data_q_3','data_q_4','data_q_5','data_q_6','data_q_7','data_q_8','data_q_9','data_q_10','data_q_11',
                'data_qd_0','data_qd_1','data_qd_2','data_qd_3','data_qd_4','data_qd_5','data_qd_6','data_qd_7','data_qd_8','data_qd_9','data_qd_10','data_qd_11',
                'data_p_0','data_p_1','data_p_2','data_p_3','data_p_4','data_p_5','data_p_6','data_p_7','data_p_8','data_p_9','data_p_10','data_p_11',
                'data_v_0','data_v_1','data_v_2','data_v_3','data_v_4','data_v_5','data_v_6','data_v_7','data_v_8','data_v_9','data_v_10','data_v_11',
                'data_tau_est_0','data_tau_est_1','data_tau_est_2','data_tau_est_3','data_tau_est_4','data_tau_est_5','data_tau_est_6','data_tau_est_7','data_tau_est_8','data_tau_est_9','data_tau_est_10','data_tau_est_11',
                'J0_0', 'J0_1', 'J0_2','J0_3','J0_4','J0_5','J0_6','J0_7','J0_8',
                'J1_0', 'J1_1', 'J1_2','J1_3','J1_4','J1_5','J1_6','J1_7','J1_8',
                'J2_0', 'J2_1', 'J2_2','J2_3','J2_4','J2_5','J2_6','J2_7','J2_8',
                'J3_0', 'J3_1', 'J3_2','J3_3','J3_4','J3_5','J3_6','J3_7','J3_8',
                'p_0', 'p_1', 'p_2',
                'vWorld_0', 'vWorld_1', 'vWorld_2',
                'vBody_0', 'vBody_1', 'vBody_2',
                'rpy_0', 'rpy_1', 'rpy_2',
                'omegaBody_0', 'omegaBody_1', 'omegaBody_2',
                'omegaWorld_0', 'omegaWorld_1', 'omegaWorld_2',
                'quat_0', 'quat_1', 'quat_2', 'quat_3',
                'pBody_des_0','pBody_des_1','pBody_des_2',
                'vBody_des_0','vBody_des_1','vBody_des_2',
                'aBody_des_0','aBody_des_1','aBody_des_2',
                'pBody_rpy_des_0','pBody_rpy_des_1','pBody_rpy_des_2',
                'vBody_ori_des_0','vBody_ori_des_1','vBody_ori_des_2',
                'pFoot_des_0','pFoot_des_1','pFoot_des_2','pFoot_des_3','pFoot_des_4','pFoot_des_5','pFoot_des_6','pFoot_des_7','pFoot_des_8','pFoot_des_9','pFoot_des_10','pFoot_des_11',
                'vFoot_des_0','vFoot_des_1','vFoot_des_2','vFoot_des_3','vFoot_des_4','vFoot_des_5','vFoot_des_6','vFoot_des_7','vFoot_des_8','vFoot_des_9','vFoot_des_10','vFoot_des_11',
                'aFoot_des_0','aFoot_des_1','aFoot_des_2','aFoot_des_3','aFoot_des_4','aFoot_des_5','aFoot_des_6','aFoot_des_7','aFoot_des_8','aFoot_des_9','aFoot_des_10','aFoot_des_11',
                'Fr_des_0','Fr_des_1','Fr_des_2','Fr_des_3','Fr_des_4','Fr_des_5','Fr_des_6','Fr_des_7','Fr_des_8','Fr_des_9','Fr_des_10','Fr_des_11',
                'contact_state_0', 'contact_state_1', 'contact_state_2', 'contact_state_3'
                ]
        self.ctrl_cmd_ready  = False
        self.ctrl_data_ready = False
        self.state_est_ready = False
        self.mpc_state_data_ready = False

    """
    struct leg_control_command_lcmt {
        float tau_ff[12];
        float f_ff[12];
        float q_des[12];
        float qd_des[12];
        float p_des[12];
        float v_des[12];
        float kp_cartesian[12];
        float kd_cartesian[12];
        float kp_joint[12];
        float kd_joint[12];
    }
    """
    def ctrl_cmd_handler(self, channel, data):
        msg = leg_control_command_lcmt.decode(data)
        
        # Fill in the corresponding section of buffer and set flag
        # global ctrl_cmd_ready
        # global buffer

        self.buffer[0:11]  = msg.tau_ff
        self.buffer[12:23] = msg.f_ff
        self.buffer[24:35] = msg.q_des
        self.buffer[36:47] = msg.qd_des
        self.buffer[48:59] = msg.p_des
        self.buffer[60:71] = msg.v_des
        self.buffer[72:83] = msg.kp_cartesian
        self.buffer[84:95] = msg.kd_cartesian
        self.buffer[96:107] = msg.kp_joint
        self.buffer[108:119] = msg.kd_joint

        self.ctrl_cmd_ready = True

    """
    struct leg_control_data_lcmt {
        float q[12];
        float qd[12];
        float p[12];
        float v[12];
        float tau_est[12];
        float jacobian0[9];
        float jacobian1[9];
        float jacobian2[9];
        float jacobian3[9];
    }
    """
    def ctrl_data_handler(self, channel, data):
        msg = leg_control_data_lcmt.decode(data)

        # Fill in corresponding section of buffer and set flag
        # global ctrl_data_ready
        # global buffer

        # self.buffer[72:83]   = msg.q
        # self.buffer[84:95]   = msg.qd
        # self.buffer[96:107]  = msg.p
        # self.buffer[108:119] = msg.v
        # self.buffer[120:131] = msg.tau_est
        # self.buffer[132:140] = msg.jacobian0
        # self.buffer[141:149] = msg.jacobian1
        # self.buffer[150:158] = msg.jacobian2
        # self.buffer[159:167] = msg.jacobian3
        self.buffer[120:131] = msg.q
        self.buffer[132:143] = msg.qd
        self.buffer[144:155] = msg.p
        self.buffer[156:167] = msg.v
        self.buffer[168:179] = msg.tau_est
        self.buffer[180:188] = msg.jacobian0
        self.buffer[189:197] = msg.jacobian1
        self.buffer[198:206] = msg.jacobian2
        self.buffer[207:215] = msg.jacobian3

        self.ctrl_data_ready = True



    """
    struct state_estimator_lcmt {
        float p[3];
        float vWorld[3];
        float vBody[3];
        float rpy[3];
        float omegaBody[3];
        float omegaWorld[3];
        float quat[4];
    }
    """
    def state_estim_handler(self, channel, data):
        msg = state_estimator_lcmt.decode(data)

        # self.buffer[168:170] = msg.p
        # self.buffer[171:173] = msg.vWorld
        # self.buffer[174:176] = msg.vBody
        # self.buffer[177:179] = msg.rpy
        # self.buffer[180:182] = msg.omegaBody
        # self.buffer[183:185] = msg.omegaWorld
        # self.buffer[186:189] = msg.quat
        self.buffer[216:218] = msg.p
        self.buffer[219:221] = msg.vWorld
        self.buffer[222:224] = msg.vBody
        self.buffer[225:227] = msg.rpy
        self.buffer[228:230] = msg.omegaBody
        self.buffer[231:233] = msg.omegaWorld
        self.buffer[234:237] = msg.quat

        self.state_est_ready = True

    """
    struct mpc_state_data_t
    {
        float pBody_des[3];
        float vBody_des[3];
        float aBody_des[3];
        
        float pBody_rpy_des[3];
        float vBody_ori_des[3];
        
        float pFoot_des[12];
        float vFoot_des[12];
        float aFoot_des[12];
        float Fr_des[12];

        float contact_state[4];
    }
    """
    def mpc_data_handler(self, channel, data):
        msg = mpc_state_data_t.decode(data)

        self.buffer[238:240] = msg.pBody_des
        self.buffer[241:243] = msg.vBody_des
        self.buffer[244:246] = msg.aBody_des
        self.buffer[247:249] = msg.pBody_rpy_des
        self.buffer[250:252] = msg.vBody_ori_des
        self.buffer[253:264] = msg.pFoot_des
        self.buffer[265:276] = msg.vFoot_des
        self.buffer[277:288] = msg.aFoot_des
        self.buffer[289:300] = msg.Fr_des
        self.buffer[301:304] = msg.contact_state

        self.mpc_state_data_ready = True


handler = Handler()          
# print(len(handler.buffer))          
# print(len(handler.header))          
# f = open("/home/ursk/muadquad_data/mq_telem" + time.strftime("_%d_%m_%Y_%H-%M-%S") + ".csv",'w+')
# f = open("/home/adsm/mq_telem/mq_telem" + time.strftime("_%d_%m_%Y_%H-%M-%S") + ".csv",'w+')
f = open("/home/mrako/Documents/EMBIR/mq_telem" + time.strftime("_%d_%m_%Y_%H-%M-%S") + ".csv",'w+')
writer = csv.writer(f)
writer.writerow(handler.header)

# ctrl_cmd_ready = False
# ctrl_data_ready = False

lc = lcm.LCM()
lc_mpc = lcm.LCM()
subscription = lc.subscribe("leg_control_command", handler.ctrl_cmd_handler)
subscription = lc.subscribe("leg_control_data", handler.ctrl_data_handler)
subscription = lc.subscribe("state_estimator", handler.state_estim_handler)
subscription = lc_mpc.subscribe("mpc_data", handler.mpc_data_handler)

iter = 0
start_time = time.time()
try:
    while True:
        lc.handle_timeout(100)
        
        if handler.ctrl_cmd_ready and handler.ctrl_data_ready and handler.state_est_ready:
            lc_mpc.handle_timeout(1)
            cur_time = time.time() - start_time
            buf2 = [cur_time] + handler.buffer[:305]
            # print(len(handler.buffer))
            writer.writerow([round(e, 4) for e in buf2])
            handler.buffer = [0 for x in range(305)]
            handler.ctrl_cmd_ready = False
            handler.ctrl_data_ready = False
            handler.state_est_ready = False
            handler.mpc_state_data_ready = False

        if iter % 300 == 0:
            print("logging is still alive")

        iter += 1
except KeyboardInterrupt:
    f.close()