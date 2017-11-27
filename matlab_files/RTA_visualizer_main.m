% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Plot simulated realtime data
% 
% stefano.orsolini@gmail.com
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%% known parameters of input signal

% sampling frequency
params.Fs = 160;

%% visualization parameters
% set amplitude axis: true->static, false->dynamic
params.s_aaxis = false;

% frames per second
params.FPS = 25;
% time interval to plot in seconds
params.t_show = 4;


%% function call

RTA_visualizer(params);
