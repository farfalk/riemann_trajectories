% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Plot simulated realtime data
% 
% stefano.orsolini@gmail.com
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% sampling frequency
params.Fs = 160;
% analysis time window in seconds
params.t_show = 5;

% set amplitude axis: true->static, false->dynamic
params.s_aaxis = false;
% frames per second
params.FPS = 25;
% show hyperplane
params.show_plane = true;
% Z offset
params.Zp_off = 0;

% function call
RTA_visualizer(params);
