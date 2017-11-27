function RTA_visualizer(params)

% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Plot simulated realtime data
%
% stefano.orsolini@gmail.com
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

close all

% fname = dir('*.dat');
% s = importdata(fname(end).name);
% % cosider ognly one channel
% s = s(:,1);

X1 = importdata('X1.dat');
X2 = importdata('X2.dat');
X3 = importdata('X3.dat');

% total number of samples
s_len = length(X1);
do_loop = true;

% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% instance graphics
% ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

x_label = 'auto-cov A';
y_label = 'auto-cov B';
z_label = 'cross-cov AB';

h0 = figure;

% buffer size in samples
b_span = (params.t_show * params.Fs);
% instance buffer with initial value zero
b_1 = zeros(b_span,1);
b_2 = zeros(b_span,1);
b_3 = zeros(b_span,1);
% instance reverse time axis in seconds
t_b = linspace(-params.t_show,0,b_span);

% riemann space basis
b_11_ry = zeros(b_span,1);
b_12_ry = zeros(b_span,1);
b_22_ry = zeros(b_span,1);
b_23_ry = zeros(b_span,1);
b_33_ry = zeros(b_span,1);
b_31_ry = zeros(b_span,1);

f1 = plot3(b_11_ry, b_22_ry, b_12_ry,'LineWidth',1.5);
hold on
f2 = plot3(b_22_ry, b_33_ry, b_23_ry,'LineWidth',1.5);
f3 = plot3(b_11_ry, b_33_ry, b_31_ry,'LineWidth',1.5);
xlabel(x_label)
ylabel(y_label)
zlabel(z_label)
axis square

drawnow

% modified colormap
custom_cmap = [flipud(uint8(winter(b_span)*255)) uint8(ones(b_span,1))].';
set(f1.Edge,'ColorBinding','interpolated','ColorData',custom_cmap)

custom_cmap = [flipud(uint8(autumn(b_span)*255)) uint8(ones(b_span,1))].';
set(f2.Edge,'ColorBinding','interpolated','ColorData',custom_cmap)

custom_cmap = [flipud(uint8(copper(b_span)*255)) uint8(ones(b_span,1))].';
set(f3.Edge,'ColorBinding','interpolated','ColorData',custom_cmap)

%frame counter
n = 0;
n_rate = floor(params.Fs/params.FPS);

%signal counter
i = 0;

% keep alive variable
keep = 1;
while keep && i ~= s_len
    % read new sample removing continuous component noise
    i = i+1;
    
    % append new timepoint, while removing the oldest
    b_1 = [b_1(2:end,:); X1(i)];
    b_2 = [b_2(2:end,:); X2(i)];
    b_3 = [b_3(2:end,:); X3(i)];
    
    % riemann space components
    xcov_seq = xcov(b_1);
    b_11_ry = [b_11_ry(2:end,:); xcov_seq(b_span)];
    xcov_seq = xcov(b_1,b_2);
    b_12_ry = [b_12_ry(2:end,:); xcov_seq(b_span)];
    xcov_seq = xcov(b_2);
    b_22_ry = [b_22_ry(2:end,:); xcov_seq(b_span)];
    xcov_seq = xcov(b_2,b_3);
    b_23_ry = [b_23_ry(2:end,:); xcov_seq(b_span)];
    xcov_seq = xcov(b_3);
    b_33_ry = [b_33_ry(2:end,:); xcov_seq(b_span)];
    xcov_seq = xcov(b_3,b_1);
    b_31_ry = [b_31_ry(2:end,:); xcov_seq(b_span)];
    
    % increment video frame counter
    n = n+1;
    
    if sum(~ishandle(h0))
        % if plot is closed exit while loop
        keep = 0;
    elseif n == n_rate
        % reset video frame counter
        n = 0;
        
        % update f1
        set(f1,'XData',b_11_ry);
        set(f1,'YData',b_22_ry);
        set(f1,'ZData',b_12_ry);
        
        % update f2
        set(f2, 'XData', b_22_ry);
        set(f2, 'YData', b_33_ry);
        set(f2, 'ZData', b_23_ry);
        
        % update f3
        set(f3, 'XData', b_11_ry);
        set(f3, 'YData', b_33_ry);
        set(f3, 'ZData', b_31_ry);
        
        drawnow
    end
    
    if do_loop && (i == (s_len-1))
        i = 1;
    end
end
