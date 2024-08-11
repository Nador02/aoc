_SOURCE_KEY = "source"
_DEST_KEY = "dest"

class FarmingMap():
    def __init__(self):
        self.ranges = []

    def add_range(self, source: list, dest: list):
        """Add a range to the farming map."""
        self.ranges.append({
            _SOURCE_KEY: source,
            _DEST_KEY: dest
        })
    
    def find_range_value_in(self, val: int):
        """Find what range the value falls within, return None
        if it does not fall into any.
        """
        for range_dict in self.ranges:
            source_range = range_dict[_SOURCE_KEY]
            if val >= source_range[0] and val < source_range[-1]:
                return range_dict
        return None

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
        # Empty list base case
        if len(range_to_map) == 0:
            return []
        
        # Define our low and high value and ranges for checking initial base cases
        low = range_to_map[0]
        high = range_to_map[-1]
        low_range = self.find_range_value_in(low)
        high_range = self.find_range_value_in(high)

        # Check our two key base cases:
        # 1. If neither the high or low value are in any ranges, we just return the intial range
        # 2. If both are in the same range, no splitting is neededm, so we map those values and return the new mapped range
        if low_range == high_range:
            if low_range is None:
                return [range_to_map]
            else:
                mapped_low = low_range[_DEST_KEY][low_range[_SOURCE_KEY].index(low)]
                mapped_high = low_range[_DEST_KEY][low_range[_SOURCE_KEY].index(high)+1]
                return [range(mapped_low, mapped_high)]
            
        # Otherwise we keep splitting up our range till nothing is left
        mapped_ranges = []
        for range_dict in self.ranges:
            source_range = range_dict[_SOURCE_KEY]
            dest_range = range_dict[_DEST_KEY]

            # Case 1 is high of the source range overlaps with the lower end of ours
            if source_range[-1] >= low and source_range[0] < low:
                bottom_idx = -(source_range[-1]-low)
                mapped_ranges.append(range(dest_range[bottom_idx], dest_range[-1]+1))
                split_idx = range_to_map.index(source_range[-1])
                return mapped_ranges + self.map_range(range_to_map[split_idx+1:])
            
            # Case 2 is low of the source range overlaps with the higher end of ours
            if source_range[0] <= high and source_range[-1] > high:
                top_idx = high-source_range[0]
                mapped_ranges.append(range(dest_range[0], dest_range[top_idx]+1))
                split_idx = range_to_map.index(source_range[0])
                return mapped_ranges + self.map_range(range_to_map[:split_idx])
            
            # Case 3 is the range is completely inside ours, so we will have two recursive calls
            # one for the low remaining range and one for the high
            if source_range[0] >= low and source_range[-1] <= high:
                mapped_ranges.append(dest_range)
                split_indices = [range_to_map.index(source_range[0]), range_to_map.index(source_range[-1])]
                high_mapped_range = self.map_range(range_to_map[split_indices[1]+1:])
                low_mapped_range = self.map_range(range_to_map[:split_indices[0]])
                return mapped_ranges + low_mapped_range + high_mapped_range
    
    def map_ranges(self, ranges_to_map: list[list[int]]):
        """Get the corresponding values returned after mapping."""
        return [self.map_range(range_to_map) for range_to_map in ranges_to_map]

