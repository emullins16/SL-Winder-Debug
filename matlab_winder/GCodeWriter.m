classdef GCodeWriter
    properties
        filename
    end

    methods
        function obj = GCodeWriter(filename)
            obj.filename = filename;
        end

        function write(obj, gcode)
            [pathstr,~,~] = fileparts(obj.filename);

            if ~isempty(pathstr) && ~exist(pathstr, 'dir')
                mkdir(pathstr);
            end

            fid = fopen(obj.filename, 'w');

            if fid == -1
                error("Could not open file: %s", obj.filename);
            end

            for i = 1:length(gcode)
                fprintf(fid, '%s\n', gcode(i));
            end

            fclose(fid);
        end
    end
end
