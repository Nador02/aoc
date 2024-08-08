import numpy as np

_SOURCE_KEY = "source"
_DEST_KEY = "dest"

class FarmingMap():
    def __init__(self):
        self.ranges = []
        self.max_source_val = -np.inf

    def add_range(self, source: list, dest: list):
        """Add a range to the farming map."""
        self.ranges.append({
            _SOURCE_KEY: source,
            _DEST_KEY: dest
        })
        if source[-1] > self.max_source_val:
            self.max_source_val = source[-1]
    
    def find_range_value_in(self, val: int):
        """Find what range the value falls within, return None
        if it does not fall into any.
        """
        for range in self.ranges:
            if val in range[_SOURCE_KEY]:
                return range
        return None
    
    def find_pseudo_range(self, val: int):
        """Find our "pseudo range" which is effectively just the local range
        of values that do not have a range.
        """
        next_closest_range_floor = None
        diff = np.inf
        for range_dict in self.ranges:
            print(range_dict["source"])
            if range_dict[_SOURCE_KEY][0] - val < diff and range_dict[_SOURCE_KEY][0] - val > 0:
                diff = range_dict[_SOURCE_KEY][0] - val
                next_closest_range_floor = range_dict[_SOURCE_KEY][0]

        if next_closest_range_floor is None:
            return range(val, self.max_source_val+1)

        return range(val, next_closest_range_floor)

    def map_value(self, val: int):
        """Get the corresponding value returned after mapping.
        If it is not found within any source range, return the original val.
        """
        range = self.find_range_value_in(val)
        if range is None:
            return val
        return range[_DEST_KEY][range[_SOURCE_KEY].index(val)]
    
    def map_values(self, values: list[int]):
        """Get the corresponding values returned after mapping."""
        return [self.map_value(val) for val in values]

    def map_range(self, range_to_map: list[int]):
        """Map a range based on the given farming map ranges.
        If a range does not entirely fall within a single farming map range,
        we need to split it into multiple ranges and return all of them. 
        """
        # low = range_to_map[0]
        # high = range_to_map[-1]
        # low_range_dict = self.find_range_value_in(low)
        # low_range = low_range_dict[_SOURCE_KEY] if low_range_dict is not None else self.find_pseudo_range(low)
        # high_range_dict = self.find_range_value_in(high)
        # high_range = high_range_dict[_SOURCE_KEY] if high_range_dict is not None else self.find_pseudo_range(high)

        # # If the whole range is within a single range in our map, return
        # # the new mapped range
        # if low_range == high_range:
        #     return [range(self.map_value(low), self.map_value(high)+1)]
        
        # split_ranges = []
        # split_point = low_range[-1]
        # # If not, we need to split it, so grab the split point
        # while split_point < high:
        #     # Apppend the split range
        #     split_ranges.append(range(self.map_value(low), self.map_value(split_point)+1))

        #     # Define the next split point
        #     low = split_point + 1
        #     split_point_dict = self.find_range_value_in(split_point+1)
        #     split_range = split_point_dict[_SOURCE_KEY] if split_point_dict is not None else self.find_pseudo_range(split_point+1)
        #     print(split_range)
        #     split_point = split_range[-1]
        
        # # Append the final split range and return the result list
        # split_ranges.append(range(self.map_value(low), self.map_value(high)))
        # return split_ranges

    def map_ranges(self, ranges: list[list[int]]):
        """Get the corresponding values returned after mapping."""
        return [self.map_range(range) for range in ranges]

