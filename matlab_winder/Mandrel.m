classdef Mandrel
    properties
        diameter    
        length  
    end

    methods
        function obj = Mandrel(diameter, length)
            obj.diameter = diameter;
            obj.length = length;
        end

        function C = circumference(obj)
            C = pi * obj.diameter;
        end
    end
end
