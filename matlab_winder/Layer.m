classdef Layer
    properties
        angle % winding angle in degrees
        passes % number of passes
        type = "helical"
    end

    methods
        function obj = Layer(angle, passes, type)
            obj.angle = angle;
            obj.passes = passes;

            if nargin > 2
                obj.type = type;
            end
        end
    end
end
