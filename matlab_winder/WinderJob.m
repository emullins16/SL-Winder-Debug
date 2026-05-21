classdef WinderJob < handle
    properties
        machine
        mandrel
        layers = Layer.empty
    end

    methods
        function obj = WinderJob(machine, mandrel)
            obj.machine = machine;
            obj.mandrel = mandrel;
        end

        function addLayer(obj, angle, passes)
            obj.layers(end+1) = Layer(angle, passes, "helical");
        end

        function addHoopLayer(obj, passes)
            obj.layers(end+1) = Layer(90, passes, "hoop");
        end

        function gcode = generateGCode(obj)
            gcode = strings(0,1);

            if obj.machine.units == "in"
                gcode(end+1,1) = "G20 ; units in inches";
            else
                gcode(end+1,1) = "G21 ; units in mm";
            end

            gcode(end+1,1) = "G90 ; absolute positioning";
            gcode(end+1,1) = "G92 " + obj.machine.linAxis + "0 " + obj.machine.rotAxis + "0 ; set current position as zero";
            gcode(end+1,1) = "G0 " + obj.machine.linAxis + "0 " + obj.machine.rotAxis + "0";

            currentRot = 0; % mandrel revs
            currentLin = 0; % carriage position

            for i = 1:length(obj.layers)
                layer = obj.layers(i);

                if layer.type == "helical"
                    [newLines, currentRot, currentLin] = obj.generateHelicalLayer(layer, currentRot, currentLin);
                    gcode = [gcode; newLines(:)];

                elseif layer.type == "hoop"
                    [newLines, currentRot, currentLin] = obj.generateHoopLayer(layer, currentRot, currentLin);
                    gcode = [gcode; newLines(:)];
                end
            end

            gcode(end+1,1) = "M30 ; end program";
        end

        function [lines, currentRot, currentLin] = generateHelicalLayer(obj, layer, currentRot, currentLin)
            lines = strings(0,1);

            theta = deg2rad(abs(layer.angle));
            C = obj.mandrel.circumference();
            L = obj.mandrel.length;

            % axial travel per mandrel revolution
            lead = C / tan(theta);

            % mandrel revolutions needed for one full carriage pass
            deltaRot = L / lead;

            for p = 1:layer.passes
                % Alternate carriage endpoint each pass
                if mod(p,2) == 1
                    nextLin = L;
                else
                    nextLin = 0;
                end

                % Positive/negative angle controls mandrel rotation direction
                currentRot = currentRot + deltaRot;

                currentLin = nextLin;

                cmdRot = currentRot * obj.machine.rotScale;
                cmdLin = currentLin * obj.machine.linScale;

                lines(end+1,1) = ...
                    "G1 " + obj.machine.rotAxis + num2str(cmdRot, "%.4f") + ...
                    " " + obj.machine.linAxis + num2str(cmdLin, "%.4f") + ...
                    " F" + num2str(obj.machine.feedRate);
            end
        end

        function [lines, currentRot, currentLin] = generateHoopLayer(obj, layer, currentRot, currentLin)
            lines = strings(0,1);

            for p = 1:layer.passes
                currentRot = currentRot + 1; % one mandrel revolution

                cmdRot = currentRot * obj.machine.rotScale;
                cmdLin = currentLin * obj.machine.linScale;

                lines(end+1,1) = ...
                    "G1 " + obj.machine.rotAxis + num2str(cmdRot, "%.4f") + ...
                    " " + obj.machine.linAxis + num2str(cmdLin, "%.4f") + ...
                    " F" + num2str(obj.machine.feedRate);
            end
        end
    end
end
