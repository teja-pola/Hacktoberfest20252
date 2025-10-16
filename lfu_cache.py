# LeetCode 460. LFU Cache
# Approach: Use two-level mapping: key->(value,freq) and freq->OrderedDict of keys.
# On get/put update frequency and move key to next freq's OrderedDict.
# Time: O(1) amortized for get/put. Space: O(capacity)

from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val_freq = {}  # key -> (value, freq)
        self.freq_to_keys = defaultdict(OrderedDict)  # freq -> OrderedDict of keys (preserve recency)
        self.min_freq = 0

    def _update_freq(self, key):
        val, freq = self.key_to_val_freq[key]
        # remove from current freq OrderedDict
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        # add to freq+1
        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.key_to_val_freq[key] = (val, new_freq)

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        self._update_freq(key)
        return self.key_to_val_freq[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.key_to_val_freq:
            # update value and freq
            _, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = (value, freq)
            self._update_freq(key)
            return
        if len(self.key_to_val_freq) >= self.capacity:
            # evict least frequently used key; for ties evict least recently used (OrderedDict order)
            key_to_evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[key_to_evict]
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
        # insert new key with freq 1
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

# quick smoke test
if __name__ == "__main__":
    c = LFUCache(2)
    c.put(1,1)
    c.put(2,2)
    print(c.get(1))  # 1
    c.put(3,3)       # evicts key 2
    print(c.get(2))  # -1
    print(c.get(3))  # 3
