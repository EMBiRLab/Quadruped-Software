
standup_kp400 = "data\mq_telem_04_05_2022_15-01-20.csv";
balancestand_attemp1 = "data\mq_telem_04_05_2022_18-17-45.csv";
balancestand_attemp2 = "data\mq_telem_04_05_2022_18-34-10.csv";
balancestand_attemp3 = "data\mq_telem_04_05_2022_19-54-04.csv"; % leg broke
balancestand_attemp4 = "data\mq_telem_04_05_2022_22-10-42.csv"; % flailing leg, killed
balancestand_attemp5 = "data\mq_telem_04_05_2022_22-25-57.csv"; % flailing, no kill, estop (orientation check fail)

balancestand_attemp9 = "data\mq_telem_05_05_2022_00-16-00.csv";

state_est_debug1 = "data\mq_telem_05_05_2022_01-21-48.csv";
state_est_debug2 = "data\mq_telem_05_05_2022_02-15-42.csv";

pushup_attempt1 = "data\mq_telem_05_05_2022_19-07-41.csv";
pushup_attempt2 = "data\mq_telem_05_05_2022_19-39-58.csv";

pushup_attempt3 = "data\mq_telem_05_05_2022_20-24-59.csv";

pushup_attempt4 = "data\mq_telem_05_05_2022_21-40-46.csv";

pushup_attempt5 = "data\mq_telem_05_05_2022_22-04-05.csv"; % lateral axis link snapped! cartesian kp=500, kd=8

grf_tes1 = "data\mq_telem_06_05_2022_12-25-36.csv";

T = readtable(grf_tes1);
headers = T.Properties.VariableNames;
%%
set(0, 'DefaultTextInterpreter', 'latex');
set(0, 'DefaultLegendInterpreter', 'latex');
set(0, 'DefaultAxesTickLabelInterpreter', 'latex');


figure;

hold on;

plot3(T.data_p_0, T.data_p_1, T.data_p_2, '-')
plot3(T.data_p_3, T.data_p_4, T.data_p_5, '-')
plot3(T.data_p_6, T.data_p_7, T.data_p_8, '-')
plot3(T.data_p_9, T.data_p_10, T.data_p_11, '-')

legend(["leg 0", "leg 1", "leg 2", "leg 3"], 'Location','best')
grid on
daspect([1 1 1])
xlabel("x [m] (fore-aft)")
ylabel("y [m] (latero-medial)")
zlabel("z [m] (vertical)")
view([-140 30])

hold off;

%%
figure;
hold on
plot(T.data_p_2, '-')
plot(T.data_p_5, '-')
plot(T.data_p_8, '-')
plot(T.data_p_11, '-')
legend()
%%

num_rows = size(T,1);

dmask = false(num_rows, 1);
dmask(1:1:end) = 1;

% dmask(1:8680) = 0;
% dmask(8820:end) = 0;

num_samples = sum(dmask);

down_x = T.data_p_0(dmask);
down_y = T.data_p_1(dmask);
down_z = T.data_p_2(dmask);

q0 = T.data_q_0(dmask);
q1 = T.data_q_1(dmask);
q2 = T.data_q_2(dmask);

tau0 = T.cmd_tau_ff_0(dmask);
tau1 = T.cmd_tau_ff_1(dmask);
tau2 = T.cmd_tau_ff_2(dmask);

fff0 = T.cmd_f_ff_0(dmask);
fff1 = T.cmd_f_ff_1(dmask);
fff2 = T.cmd_f_ff_2(dmask);

grf_x = down_x;
grf_y = down_x;
grf_z = down_x;

fff_x = down_x;
fff_y = down_x;
fff_z = down_x;

deltaJ = zeros([num_samples, 9]);
idx_begin =  find(ismember(headers,"J0_0"));
idx_end =  find(ismember(headers,"J0_8"));
Jcpp = table2array(T(:,idx_begin:idx_end));
Jcpp_down = Jcpp(dmask,:);

for ii = 1:num_samples
    q_vec = [q0(ii), q1(ii), q2(ii)];
    sideSign = 1;
    J = foot_jacobian(q_vec, sideSign);
    J_vec = reshape(J', [1,9]); % undo with reshape(J_vec, [3,3])'
    deltaJ(ii,:) = J_vec - Jcpp_down(ii,:);
    u_vec = [tau0(ii); tau1(ii); tau2(ii)];
    grf = inv(J')*u_vec;

    if (ii == 10)
        fprintf("here")
    end

    grf_x(ii) = grf(1);
    grf_y(ii) = grf(2);
    grf_z(ii) = grf(3);

    fff_x(ii) = fff0(ii);
    fff_y(ii) = fff1(ii);
    fff_z(ii) = fff2(ii);
end

%% Foot Force Plotting
figure;

hold on
plot3(T.data_p_9, T.data_p_10, T.data_p_11, '-')
plot3(down_x, down_y, down_z, 'o')

force_vec_scale = 0.003; % m per N

vec_x = down_x + force_vec_scale*grf_x;
vec_y = down_y + force_vec_scale*grf_y;
vec_z = down_z + force_vec_scale*grf_z;

vec2_x = down_x + force_vec_scale*fff_x;
vec2_y = down_y + force_vec_scale*fff_y;
vec2_z = down_z + force_vec_scale*fff_z;

for jj = 1:length(vec_x)
    dx = [down_x(jj), vec_x(jj)];
    dy = [down_y(jj), vec_y(jj)];
    dz = [down_z(jj), vec_z(jj)];

    d2x = [down_x(jj), vec2_x(jj)];
    d2y = [down_y(jj), vec2_y(jj)];
    d2z = [down_z(jj), vec2_z(jj)];

    plot3(dx, dy, dz, 'r-', 'linewidth',1)

    plot3(d2x, d2y, d2z, 'b:', 'linewidth',1)
end

plot3([0], [T.data_p_4(1)], [-0.25], 'g.', 'MarkerSize',10)

xlabel("x [m] (fore-aft)")
ylabel("y [m] (latero-medial)")
zlabel("z [m] (vertical)")

view([-140 30])
grid on
daspect([1 1 1])
hold off

%% Torque and Jacobian Traces

figure;

subplot(1,2,1)
hold on
for ii = 1:9
    plot(deltaJ(:,ii));
end
hold off

subplot(1,2,2)
hold on
for ii = 1:9
    plot(Jcpp_down(:,ii));
end
hold off;

% subplot(1,3,3)
% hold on
% for ii = 1:9
%     plot(J_vec(:,ii));
% end
% hold off;
legend()

%%

figure;

% subplot(3,1,1)
hold on
% plot(T.cmd_tau_ff_6, 'r', 'DisplayName','MIT2');
% plot(T.cmd_tau_ff_7, 'b');
% plot(T.cmd_tau_ff_8, 'k');

plot(T.cmd_tau_ff_9, 'r-', 'DisplayName','MIT3');
plot(T.cmd_tau_ff_10, 'b-');
plot(T.cmd_tau_ff_11, 'k-');
% plot(T.cmd_tau_ff_11);

% plot(T.data_tau_est_6, 'r:', 'DisplayName','MIT2');
% plot(T.data_tau_est_7, 'b:');
% plot(T.data_tau_est_8, 'k:');

plot(T.data_tau_est_9, 'r.', 'DisplayName','MIT3');
plot(T.data_tau_est_10, 'b.');
plot(T.data_tau_est_11, 'k.');

% plot(10*T.data_p_8, 'DisplayName', 'z MIT2', 'linewidth', 2);
% plot(10*T.data_p_11, 'DisplayName', 'z MIT3', 'linewidth', 2);

% plot(T.data_v_7, 'DisplayName','MIT2 vy', 'linewidth', 2);
plot(T.data_v_9, 'DisplayName','MIT3 vx', 'linewidth', 2);
plot(T.data_v_11, 'DisplayName','MIT3 vz', 'linewidth', 2);

legend();
hold off

%% Tibia torques

figure;

hold on

plot(T.cmd_tau_ff_2, '-', 'DisplayName','mit0 tau ff')
plot(T.data_tau_est_2, '.', 'DisplayName','mit0 tau est')


plot(T.cmd_tau_ff_5, '-', 'DisplayName','mit1 tau ff')
plot(T.data_tau_est_5, '.', 'DisplayName','mit1 tau est')

plot(T.cmd_tau_ff_8, '-', 'DisplayName','mit2 tau ff')
plot(T.data_tau_est_8, '.', 'DisplayName','mit2 tau est')

plot(T.cmd_tau_ff_11, '-', 'DisplayName','mit3 tau ff')
plot(T.data_tau_est_11, '.', 'DisplayName','mit3 tau est')

legend()

%%

% subplot(1,2,1)
figure;
hold on
plot(T.data_q_6, 'r')
plot(T.data_q_7, 'b')
plot(T.data_q_8, 'k')

plot(T.data_q_9, 'g')
plot(T.data_q_10, 'y')
plot(T.data_q_11, 'm')
legend()
% plot3(T.data_p_0, T.data_p_1, T.data_p_2)
% daspect([1 1 1])
% view([-140 60])
% hold off
% 
% subplot(1,2,2)
% hold on
% % plot(T.data_v_0, 'b')
% % plot(T.data_v_1, 'r')
% % plot(T.data_v_2, 'g')
% plot3(T.data_v_0, T.data_v_1, T.data_v_2)
% daspect([1 1 1])
% view([-140 60])
% hold off

%%

figure;

quats = [(T.quat_0), (T.quat_1), (T.quat_2), (T.quat_3)];
% quats = [(T.quat_1), (T.quat_2), (T.quat_3), (T.quat_0)];
% quats = [(T.quat_2), (T.quat_3), (T.quat_0), (T.quat_1)];
eulers = quat2eul(quats, "XYZ");

% eulers(:,[1,3]) = eulers(:,[1,3]) + pi;
% eulers(:,[1,3]) = mod(eulers(:,[1,3]), 2*pi);
% eulers(:,[1,3]) = eulers(:,[1,3]) - pi;

eulers(:,1) = unwrap(eulers(:,1));
eulers(:,2) = unwrap(eulers(:,2));
eulers(:,3) = unwrap(eulers(:,3));

hold on
plot(eulers(:,1), 'r');
plot(eulers(:,2), 'b');
plot(eulers(:,3), 'k');

plot(T.rpy_0, 'ro');
plot(T.rpy_1, 'bo')
plot(T.rpy_2, 'ko')
legend()
hold off