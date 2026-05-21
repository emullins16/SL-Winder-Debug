clear; clc;

machine = Machine();
machine.linAxis = "X";
machine.rotAxis = "Z";
machine.units = "in";
machine.feedRate = 150; % in/min mm/min

% for scaling axes - better to do in firmware
machine.linScale = 1;
machine.rotScale = 1;

mandrel = Mandrel(6, 20); % diameter, length

% wind
% angle, # of passes
job = WinderJob(machine, mandrel);
job.addLayer(80, 6); 
job.addHoopLayer(3);

gcode = job.generateGCode();
disp(gcode)

writer = GCodeWriter("generated_gcode/test_wind.gcode");
writer.write(gcode);
